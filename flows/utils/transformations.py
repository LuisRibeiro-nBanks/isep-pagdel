from pyspark.sql import DataFrame

def transform_batch_data(data):
    return [(id, label.lower(), value * 2) for id, label, value in data]

def transform_streaming_data(df: DataFrame) -> DataFrame:
    return df.withColumnRenamed("value", "value_transformed")
