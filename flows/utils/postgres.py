import psycopg2
from pyspark.sql import DataFrame
import pandas as pd
import numpy as np

def write_to_postgres(full_DF, table_name):
    conn = psycopg2.connect(
        dbname="postgresDB",
        user="admin",
        password="admin",
        host="postgres",
        port=5432
    )

    cursor = conn.cursor()

    full_DF["datetime"] = pd.to_datetime(full_DF["DTM_UTC"])
    full_DF["unit"] = full_DF["UNIDADE"]

    location_df = full_DF[["LOCAL", "LATITUDE", "LONGITUDE", "Type"]].drop_duplicates().reset_index(drop=True)
    location_df.rename(columns={"LOCAL": "name", "LATITUDE": "latitude", "LONGITUDE": "longitude", "Type": "sensor_type"}, inplace=True)
    location_df = get_or_create_ids(location_df, conn, cursor, "Location", ["name", "latitude", "longitude", "sensor_type"], "location_id")

    datetime_df = full_DF[["datetime", "HOUR", "DAY", "MONTH", "YEAR", "is_weekend"]].drop_duplicates().reset_index(drop=True)
    datetime_df.rename(columns={"HOUR":"hour", "DAY":"day", "MONTH":"month", "YEAR":"year"}, inplace=True)
    datetime_df = get_or_create_ids(datetime_df, conn, cursor, "Datetime", ["datetime", "hour", "day", "month", "year", "is_weekend"], "datetime_id")

    parameter_df = full_DF[["PARAMETRO", "unit", "Type"]].drop_duplicates().reset_index(drop=True)
    parameter_df.rename(columns={"PARAMETRO": "parameter_name", "Type": "type"}, inplace=True)
    parameter_df = get_or_create_ids(parameter_df, conn, cursor, "Parameter", ["parameter_name", "unit", "type"], "parameter_id")

    full_DF.rename(columns={"LOCAL": "name", "LATITUDE": "latitude", "LONGITUDE": "longitude", "PARAMETRO": "parameter_name", "Type": "type"}, inplace=True)

    full_DF = full_DF.merge(location_df, on=["name", "latitude", "longitude", "sensor_type"])
    full_DF = full_DF.merge(datetime_df, on=["datetime", "hour", "day", "month", "year", "is_weekend"])
    full_DF = full_DF.merge(parameter_df, on=["parameter_name", "unit", "type"])

    fact_df = full_DF[["datetime_id", "location_id", "parameter_id", "VALOR", "unit"]].rename(columns={"VALOR": "value"})
    fact_df = fact_df.drop_duplicates(subset=["datetime_id", "location_id", "parameter_id"])

    validate_fact(fact_df, conn)

    #for row in data:
    #    cur.execute(f"INSERT INTO {table_name} VALUES (%s, %s, %s)", row)
   
    conn.commit()
    cursor.close()
    conn.close()



def get_or_create_ids(df, conn, cursor, table_name, unique_cols, id_col):
    if table_name == "Datetime":
        existing = pd.read_sql(f"SELECT {id_col}, {', '.join(unique_cols)} FROM {table_name}", conn.engine, parse_dates=["datetime"])
    else:
        existing = pd.read_sql(f"SELECT {id_col}, {', '.join(unique_cols)} FROM {table_name}", conn.engine)

    merged = df.merge(existing, on=unique_cols, how="left")
    new_rows = merged[merged[id_col].isna()].copy()

    if not new_rows.empty:
        cursor.execute(f"SELECT MAX({id_col}) FROM {table_name}")
        max_id = cursor.fetchone()[0] or 0
        new_rows[id_col] = range(max_id + 1, max_id + 1 + len(new_rows))
        insert_cols = [id_col] + unique_cols
        try:
            new_rows[insert_cols].to_sql(table_name, conn.engine, index=False, if_exists="append", method='multi')
        except Exception as e:
            print(f"Error inserting into {table_name}: {e}")
            raise

    return pd.concat([merged[merged[id_col].notna()], new_rows], ignore_index=True)




def validate_fact(fact_df, db_connector):
    query = "SELECT datetime_id, location_id, parameter_id FROM Fact_Measurements"
    existing_facts = pd.read_sql(query, db_connector.engine)

    fact_df = fact_df.merge(existing_facts, on=["datetime_id", "location_id", "parameter_id"], how="left", indicator=True)
    fact_df = fact_df[fact_df["_merge"] == "left_only"].drop(columns=["_merge"])

    if not fact_df.empty:
        print(f"Fact_Measurements: {fact_df.shape[0]} new rows added.")
        fact_df.to_sql("Fact_Measurements", db_connector.engine, index=False, if_exists="append", method='multi')
    else:
        print("No new measurements to insert.")

