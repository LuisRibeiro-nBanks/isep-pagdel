from prefect import flow, task
from utils.postgres import write_to_postgres
from utils.transformations import transform_batch_data, clean_data

@task
def ingest_batch_data():
    air_folder = "/flows/datasets/air-quality"
    traffic_folder = "/flows/datasets/road-traffic"
    return [air_folder, traffic_folder]

@task
def transform(data_location):
    air_folder = data_location[0]
    traffic_folder = data_location[1]
    return clean_data(air_folder, traffic_folder)
    #return transform_batch_data(data)

@task
def load_to_postgres(data):
    write_to_postgres(data, table_name="batch_table")

@flow(name="Batch Flow")
def batch_data_flow():
    data_location = ingest_batch_data()
    transformed = transform(data_location)
    load_to_postgres(transformed)
