import pandas as pd
import numpy as np
import os


########################### TEST DB ######################
from connect_db import TestDBConnector
########################### TEST DB ######################


def clean_air_data(air_DF, total_air_DF):
    cleaned_air_DF = air_DF[['DTM_UTC', 'LOCAL', 'LATITUDE', 'LONGITUDE', 'PARAMETRO', 'UNIDADE', 'VALOR']]
    cleaned_air_DF['Type'] = 'AIR QUALITY'

    # For some reason there are a random amount of spaces appearing in random entries
    cleaned_air_DF['UNIDADE'] = cleaned_air_DF['UNIDADE'].str.strip()

    # Set the date to datetime and split it by YEAR - MONTH - DAY - HOUR, for the Time table
    cleaned_air_DF['DTM_UTC'] = pd.to_datetime(cleaned_air_DF['DTM_UTC'])
    cleaned_air_DF['YEAR'] = cleaned_air_DF['DTM_UTC'].dt.year
    cleaned_air_DF['MONTH'] = cleaned_air_DF['DTM_UTC'].dt.month
    cleaned_air_DF['DAY'] = cleaned_air_DF['DTM_UTC'].dt.day
    cleaned_air_DF['HOUR'] = cleaned_air_DF['DTM_UTC'].dt.hour

    # Check if the date corresponds to a weekend
    cleaned_air_DF['is_weekend'] = cleaned_air_DF['DTM_UTC'].dt.weekday >= 5

    if not(total_air_DF.empty):
        return pd.concat([cleaned_air_DF, total_air_DF], ignore_index=True)
    else:
        return cleaned_air_DF


def clean_traffic_data(road_DF, total_traffic_DF):
    #------------------------------- ROAD TRAFFIC DATA SET CLEANING -------------------------------#
    # Only the collumns needed for the tables are selected
    cleaned_road_DF = road_DF[['DTM_UTC', 'LOCAL', 'LATITUDE', 'LONGITUDE', 'UNIDADE']]
    cleaned_road_DF['Type'] = 'ROAD TRAFFIC'


    # For some reason there are a random amount of spaces appearing in random entries
    cleaned_road_DF['UNIDADE'] = cleaned_road_DF['UNIDADE'].str.strip()

    # Get the total number of vehicles from both ways, by time (Large, Medium and Small)
    cleaned_road_DF['Total Vehicles'] = road_DF['SMO_FROMTO_TOTAL'] + road_DF['SMO_TOFROM_TOTAL']
    cleaned_road_DF['Total Large Vehicles'] = road_DF['SMO_FROMTO_L'] + road_DF['SMO_TOFROM_L']
    cleaned_road_DF['Total Medium Vehicles'] = road_DF['SMO_FROMTO_M'] + road_DF['SMO_TOFROM_M']
    cleaned_road_DF['Total Small Vehicles'] = road_DF['SMO_FROMTO_P'] + road_DF['SMO_TOFROM_P']

    # Set the date to datetime and split it by YEAR - MONTH - DAY - HOUR, for the Time table
    cleaned_road_DF['DTM_UTC'] = pd.to_datetime(cleaned_road_DF['DTM_UTC'])
    cleaned_road_DF['YEAR'] = cleaned_road_DF['DTM_UTC'].dt.year
    cleaned_road_DF['MONTH'] = cleaned_road_DF['DTM_UTC'].dt.month
    cleaned_road_DF['DAY'] = cleaned_road_DF['DTM_UTC'].dt.day
    cleaned_road_DF['HOUR'] = cleaned_road_DF['DTM_UTC'].dt.hour

    # Check if the date corresponds to a weekend
    cleaned_road_DF['is_weekend'] = cleaned_road_DF['DTM_UTC'].dt.weekday >= 5

    # Add the collumns "Parameters" and "Value"
    cleaned_road_DF = pd.melt(cleaned_road_DF,
        id_vars=['DTM_UTC', 'LOCAL', 'LATITUDE', 'LONGITUDE', 'UNIDADE','Type', 'YEAR', 'MONTH', 'DAY', 'HOUR', 'is_weekend'], 
        value_vars=['Total Vehicles', 'Total Large Vehicles', 'Total Medium Vehicles', 'Total Small Vehicles' ],                
        var_name='PARAMETRO',                                              
        value_name='VALOR')

    if not(total_traffic_DF.empty):
        return pd.concat([cleaned_road_DF, total_traffic_DF], ignore_index=True)
    else:
        return cleaned_road_DF


# This function checks if an entry already exists in the database, and swiches 
# the current id for the one in the database
def get_or_create_ids(df, conn, cursor, table_name, unique_cols, id_col):
    
    # Because of the data type, the Datetime table needs to be parsed diferently 
    if table_name == "Datetime":
        existing = pd.read_sql(
            f"SELECT {id_col}, {', '.join(unique_cols)} FROM {table_name}", conn, parse_dates=["datetime"])
    else:
        existing = pd.read_sql(
            f"SELECT {id_col}, {', '.join(unique_cols)} FROM {table_name}", conn)


    # Merges current Dataframe with the one generated from the database
    # This generates a dataframe where the new entries have a null id
    merged = df.merge(existing, on=unique_cols, how="left")
    new_rows = merged[merged[id_col].isna()].copy()


    # if there are new rows add them to the database,
    # their id value is incremented by the highest id in the respective table of the database
    if not new_rows.empty:
        cursor.execute(f"SELECT MAX({id_col}) FROM {table_name}")
        max_id = cursor.fetchone()[0] or 0
        new_rows[id_col] = range(max_id + 1, max_id + 1 + len(new_rows))

        insert_cols = [id_col] + unique_cols
        try:
            new_rows[insert_cols].to_sql(table_name, conn, index=False, if_exists="append")
        except Exception as e:
            print(f"Error inserting into {table_name}: {e}")
            raise

    # Returns the dataframe that contains the new rows added
    final = pd.concat([merged[merged[id_col].notna()], new_rows], ignore_index=True)
    return final
    
    
# Validates the fact table    
def validate_fact(fact_df, my_connector):

    #Get existing keys from DB
    query = """SELECT datetime_id, location_id, parameter_id FROM Fact_Measurements"""
    existing_facts = pd.read_sql(query, my_connector)

    #Merge and keep only new rows
    merge_collumns = ["datetime_id", "location_id", "parameter_id"]
    fact_df = fact_df.merge(existing_facts, on=merge_collumns , how="left", indicator=True)
    fact_df = fact_df[fact_df["_merge"] == "left_only"].drop(columns=["_merge"])

    #Insert only new rows
    if not fact_df.empty:
        print(f"Fact_Measurements {fact_df.shape[0]} new rows added")
        fact_df.to_sql("Fact_Measurements", my_connector, index=False, if_exists="append")
    else:
        print("No new measurements to insert.")    

def send_data(full_DF):
    
    ########################### TEST DB ######################
    my_db = TestDBConnector(r'..\database\Data\test')
    my_connector = my_db.getConnector()
    my_cursor = my_db.getCursor()
    ########################### TEST DB ######################
    
    full_DF["datetime"] = pd.to_datetime(full_DF["DTM_UTC"])
    full_DF["unit"] = full_DF["UNIDADE"]
    
    # Validate location table
    location_df = full_DF[["LOCAL", "LATITUDE", "LONGITUDE", "Type"]].drop_duplicates().reset_index(drop=True)
    location_df.rename(columns={"LOCAL": "name", 
                                "LATITUDE": "latitude", 
                                "LONGITUDE": "longitude", 
                                "Type": "sensor_type"}, inplace=True)
    location_df = get_or_create_ids(location_df, my_connector, my_cursor, "Location", ["name", "latitude", "longitude", "sensor_type"], "location_id")
    
    
    # Validate datetime table
    datetime_df = full_DF[["datetime", "HOUR", "DAY", "MONTH", "YEAR", "is_weekend"]].drop_duplicates().reset_index(drop=True)
    datetime_df.rename(columns={"datetime": "datetime" ,
                                "HOUR":"hour", 
                                "DAY":"day", 
                                "MONTH":"month", 
                                "YEAR":"year", 
                                "is_weekend":"is_weekend"}, inplace=True)
    datetime_df = get_or_create_ids(datetime_df, my_connector, my_cursor, "Datetime", ["datetime", "hour", "day", "month", "year", "is_weekend"], "datetime_id")
    
    
    # Validate parameter table
    parameter_df = full_DF[["PARAMETRO", "unit", "Type"]].drop_duplicates().reset_index(drop=True)
    parameter_df.rename(columns={"PARAMETRO": "parameter_name", 
                                 "Type": "type", 
                                 "unit":"unit"}, inplace=True)
    parameter_df = get_or_create_ids(parameter_df, my_connector, my_cursor, "Parameter", ["parameter_name", "unit", "type"], "parameter_id")


    # Validate fact_measurement table    
    full_DF.rename(columns={"LOCAL": "name", 
                            "LATITUDE": "latitude", 
                            "LONGITUDE": "longitude",
                            "datetime": "datetime" ,
                            "HOUR":"hour", 
                            "DAY":"day", 
                            "MONTH":"month", 
                            "YEAR":"year", 
                            "is_weekend":"is_weekend",
                            "PARAMETRO": "parameter_name", 
                            "Type": "type", 
                            "unit":"unit"}, inplace=True)
    
    full_DF = full_DF.merge(location_df, left_on=["name", "latitude", "longitude", "type"], right_on=["name", "latitude", "longitude", "sensor_type"])
    full_DF = full_DF.merge(datetime_df, on=["datetime", "hour", "day", "month", "year", "is_weekend"])
    full_DF = full_DF.merge(parameter_df, on=["parameter_name", "unit", "type"])

    fact_df = full_DF[["datetime_id", "location_id", "parameter_id", "VALOR", "unit"]].rename(columns={"VALOR": "value"})
    fact_df = fact_df.drop_duplicates(subset=["datetime_id", "location_id", "parameter_id"])
    
    validate_fact(fact_df, my_connector)

    ########################### TEST DB ######################
    my_connector.commit()
    my_db.closeConnection()
    ########################### TEST DB ######################
    



def clean_data(air_folder, traffic_folder):
    total_air_DF = pd.DataFrame()
    total_traffic_DF = pd.DataFrame()
    for dirpath, dirnames, filenames in os.walk(air_folder):
        for filename in filenames:
            air_path = os.path.join(dirpath, filename)
            air_DF = pd.read_csv(air_path)
            #print('############################################', air_path)
            total_air_DF = clean_air_data(air_DF, total_air_DF)


    for dirpath, dirnames, filenames in os.walk(traffic_folder):
        for filename in filenames:
            traffic_path = os.path.join(dirpath, filename)
            traffic_DF = pd.read_csv(traffic_path)

            total_traffic_DF = clean_traffic_data(traffic_DF, total_traffic_DF)
    

    #------------------------------- COMBINING DATASETS -------------------------------#
    combined_DF = pd.concat([total_air_DF, total_traffic_DF], ignore_index=True)
    #combined_DF.to_csv(r'..\datasets\results\Result.csv')
    send_data(combined_DF)
    
    







air_folder = r"..\datasets\air-quality"
traffic_folder = r"..\datasets\road-traffic"
clean_data(air_folder, traffic_folder)