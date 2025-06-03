from pyspark.sql import SparkSession
from delta.tables import DeltaTable # For advanced Delta operations like merge, update, delete

# Configuration for Delta Lake
# These configurations tell Spark how to handle Delta tables
spark_jars_packages = "io.delta:delta-spark_2.12:3.3.0" # Make sure this matches your docker-compose
spark_sql_extensions = "io.delta.sql.DeltaSparkSessionExtension"
spark_sql_catalog = "org.apache.spark.sql.delta.catalog.DeltaCatalog"

# Create SparkSession with Delta Lake configurations
spark = SparkSession.builder \
    .appName("PySparkDeltaDocker") \
    .master("spark://localhost:7077") \
    .config("spark.jars.packages", spark_jars_packages) \
    .config("spark.sql.extensions", spark_sql_extensions) \
    .config("spark.sql.catalog.spark_catalog", spark_sql_catalog) \
    .config("spark.executor.memory", "1g") \
    .config("spark.driver.memory", "1g") \
    .getOrCreate()

print("SparkSession with Delta Lake support created successfully!")

# Define a path for your Delta table.
# This path must be accessible by the Spark containers.
# Since you mounted ./data to /data in docker, we'll use /data/delta_tables
delta_table_path = "/data/my_first_delta_table"

# --- 1. Write a DataFrame to a Delta table (initial write) ---
print(f"\nWriting initial data to Delta table at {delta_table_path}")
data_initial = [("Alice", 1, "New York"), ("Bob", 2, "London"), ("Charlie", 3, "Paris")]
columns_initial = ["Name", "ID", "City"]
df_initial = spark.createDataFrame(data_initial, columns_initial)

df_initial.write \
    .format("delta") \
    .mode("overwrite") \
    .save(delta_table_path)

print("Initial Delta table created.")

# --- 2. Read from the Delta table ---
print(f"\nReading data from Delta table at {delta_table_path}")
df_read = spark.read \
    .format("delta") \
    .load(delta_table_path)
df_read.show()

# --- 3. Append more data to the Delta table ---
print(f"\nAppending new data to Delta table at {delta_table_path}")
new_data = [("David", 4, "Berlin"), ("Eve", 5, "Tokyo")]
df_new = spark.createDataFrame(new_data, columns_initial)

df_new.write \
    .format("delta") \
    .mode("append") \
    .save(delta_table_path)

print("Data appended to Delta table.")

# Read again to verify append
print(f"\nReading updated data from Delta table at {delta_table_path}")
df_updated = spark.read \
    .format("delta") \
    .load(delta_table_path)
df_updated.show()

# --- 4. Update data using DeltaTable API (requires delta.tables import) ---
print(f"\nUpdating data in Delta table at {delta_table_path}")
delta_table = DeltaTable.forPath(spark, delta_table_path)
delta_table.update(
    condition="ID = 2",
    set={"City": "'Rome'"}
)
print("Data updated.")

# Read again to verify update
print(f"\nReading data after update from Delta table at {delta_table_path}")
df_after_update = spark.read.format("delta").load(delta_table_path)
df_after_update.show()

# --- 5. Time Travel (read historical versions) ---
print(f"\nReading historical version 0 of Delta table at {delta_table_path}")
# Note: version 0 is the initial write, version 1 is after append, version 2 is after update
df_version_0 = spark.read \
    .format("delta") \
    .option("versionAsOf", 0) \
    .load(delta_table_path)
df_version_0.show()


# Stop the SparkSession
spark.stop()
print("SparkSession stopped.")