from pyspark.sql import SparkSession, DataFrame
import pandas as pd
from prefect import get_run_logger
from pyspark import SparkContext


def get_spark_session():
    # If there is an active SparkContext, stop it first to avoid 'stopped SparkContext' issues
    try:
        sc = SparkContext.getOrCreate()
        if sc._jsc.sc().isStopped():
            sc.stop()
    except Exception:
        # No active SparkContext or unable to get one; ignore and create new
        pass

    spark = SparkSession.builder \
        .appName("PostgresWriter") \
        .master("spark://spark:7077") \
        .config("spark.jars", "/custom-jars/postgresql-42.6.0.jar") \
        .config("spark.sql.extensions", "io.delta.sql.DeltaSparkSessionExtension") \
        .config("spark.sql.catalog.spark_catalog", "org.apache.spark.sql.delta.catalog.DeltaCatalog") \
        .getOrCreate()

    return spark


def write_to_postgres(full_DF: pd.DataFrame, table_name: str):
    logger = get_run_logger()

    # Use the global SparkSession instance
    spark = get_spark_session()

    db_properties = {
        "url": "jdbc:postgresql://postgres:5432/postgresDB",
        "user": "admin",
        "password": "admin",
        "driver": "org.postgresql.Driver"
    }

    logger.info("Converting full_DF to Spark DataFrame...")
    spark_df = spark.createDataFrame(full_DF)

    logger.info("Converting datetime column and extracting time components...")
    spark_df = spark_df.withColumn("datetime", spark_df["DTM_UTC"].cast("timestamp"))

    from pyspark.sql.functions import hour, dayofmonth, month, year, dayofweek, col

    spark_df = spark_df.withColumn("hour", hour(col("datetime"))) \
                       .withColumn("day", dayofmonth(col("datetime"))) \
                       .withColumn("month", month(col("datetime"))) \
                       .withColumn("year", year(col("datetime"))) \
                       .withColumn("is_weekend", (dayofweek(col("datetime")) >= 6).cast("boolean"))

    spark_df = spark_df.withColumnRenamed("UNIDADE", "unit") \
                       .withColumnRenamed("Type", "sensor_type") \
                       .withColumnRenamed("PARAMETRO", "parameter_name") \
                       .withColumnRenamed("VALOR", "value") \
                       .withColumnRenamed("LOCAL", "name") \
                       .withColumnRenamed("LATITUDE", "latitude") \
                       .withColumnRenamed("LONGITUDE", "longitude") \
                       .withColumnRenamed("type", "sensor_type")

    logger.info(f"Writing data to {table_name} using Spark JDBC...")
    spark_df.write.jdbc(
        url=db_properties["url"],
        table=table_name,
        mode="append",
        properties={k: v for k, v in db_properties.items() if k != "url"}
    )

    logger.info(f"✅ Data successfully written to {table_name}.")


# Example usage
if __name__ == "__main__":
    df = pd.read_csv("your_input_data.csv")  # Replace with your actual data source
    write_to_postgres(df, table_name="staging_batch_table")
