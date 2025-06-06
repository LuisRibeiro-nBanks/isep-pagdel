from prefect import flow, task
from utils.delta_lake import write_stream_to_delta, read_delta_table
from utils.transformations import transform_streaming_data
from utils.postgres import write_to_postgres

DELTA_PATH = "/tmp/delta/streaming_table"

@task
def ingest_streaming():
    return [(4, "D", 400), (5, "E", 500)]

@task
def write_to_delta(data):
    write_stream_to_delta(data, DELTA_PATH)
    return DELTA_PATH

@task
def transform_from_delta(delta_path):
    df = read_delta_table(delta_path)
    transformed_df = transform_streaming_data(df)
    return transformed_df.collect()

@task
def load_transformed_to_postgres(data):
    write_to_postgres(data, table_name="streaming_table")

@flow(name="Streaming Flow")
def streaming_data_flow():
    stream_data = ingest_streaming()
    delta_path = write_to_delta(stream_data)
    transformed_data = transform_from_delta(delta_path)
    load_transformed_to_postgres(transformed_data)
