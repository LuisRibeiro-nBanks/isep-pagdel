from delta import configure_spark_with_delta_pip
from pyspark.sql import SparkSession

def get_spark():
    builder = SparkSession.builder \
        .appName("DeltaLakeStreaming") \
        .config("spark.sql.extensions", "io.delta.sql.DeltaSparkSessionExtension") \
        .config("spark.sql.catalog.spark_catalog", "org.apache.spark.sql.delta.catalog.DeltaCatalog")
    return configure_spark_with_delta_pip(builder).getOrCreate()

def write_stream_to_delta(data, path):
    spark = get_spark()
    df = spark.createDataFrame(data, ["id", "label", "value"])
    df.write.format("delta").mode("append").save(path)

def read_delta_table(path):
    spark = get_spark()
    return spark.read.format("delta").load(path)
