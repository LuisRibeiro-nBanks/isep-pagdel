import pandas as pd
from sqlalchemy import create_engine
from prefect import get_run_logger

def write_to_postgres(full_DF: pd.DataFrame, table_name: str):
    logger = get_run_logger()

    db_url = "postgresql+psycopg2://admin:admin@postgres:5432/postgresDB"
    engine = create_engine(db_url)

    # Normalize column names
    full_DF.columns = [col.lower() for col in full_DF.columns]

    # Rename columns as needed (example)
    full_DF = full_DF.rename(columns={
        'dtm_utc': 'dtm_utc',  # already lowercase
        'unidade': 'unit',
        'type': 'sensor_type',
        'parametro': 'parameter_name',
        'valor': 'value',
        'local': 'name',
        'latitude': 'latitude',
        'longitude': 'longitude',
    })

    # Drop duplicate columns if any (including the time columns)
    full_DF = full_DF.loc[:,~full_DF.columns.duplicated()]

    # Drop columns if they exist before re-creating
    for col in ['hour', 'day', 'month', 'year', 'is_weekend', 'datetime']:
        if col in full_DF.columns:
            full_DF.drop(columns=[col], inplace=True)

    # Create datetime and derived columns
    full_DF['datetime'] = pd.to_datetime(full_DF['dtm_utc'])
    full_DF['hour'] = full_DF['datetime'].dt.hour
    full_DF['day'] = full_DF['datetime'].dt.day
    full_DF['month'] = full_DF['datetime'].dt.month
    full_DF['year'] = full_DF['datetime'].dt.year
    full_DF['is_weekend'] = full_DF['datetime'].dt.dayofweek >= 5

    logger.info(f"Writing data to {table_name} using pandas to_sql...")
    full_DF.to_sql(
        table_name,
        con=engine,
        if_exists='append',
        index=False,
        method='multi',
        chunksize=1000
    )

    logger.info(f"✅ Data successfully written to {table_name}.")
