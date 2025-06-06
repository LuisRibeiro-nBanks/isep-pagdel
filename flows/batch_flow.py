from prefect import flow, task
from utils.postgres import write_to_postgres
from utils.transformations import transform_batch_data

@task
def ingest_batch_data():
    return [(1, "A", 100), (2, "B", 200), (3, "C", 300)]

@task
def transform(data):
    return transform_batch_data(data)

@task
def load_to_postgres(data):
    write_to_postgres(data, table_name="batch_table")

@flow(name="Batch Flow")
def batch_data_flow():
    raw_data = ingest_batch_data()
    transformed = transform(raw_data)
    load_to_postgres(transformed)
