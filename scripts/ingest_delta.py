from delta import configure_spark_with_delta_pip
from pyspark.sql import SparkSession

builder = (
    SparkSession.builder.appName("IngestToDeltaLake")
    .config("spark.sql.extensions", "io.delta.sql.DeltaSparkSessionExtension")
    .config("spark.sql.catalog.spark_catalog", "org.apache.spark.sql.delta.catalog.DeltaCatalog")
)

spark = configure_spark_with_delta_pip(builder).getOrCreate()

data = [("Lisboa", 25), ("Porto", 22)]
df = spark.createDataFrame(data, ["cidade", "temperatura"])

df.write.format("delta").mode("overwrite").save("/tmp/delta/temperatura")

print("✅ Dados guardados no Delta Lake!")
