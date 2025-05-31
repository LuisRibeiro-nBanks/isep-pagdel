# Use the official Bitnami Spark image as the base
FROM bitnami/spark:3.3.1

# Define argument for Delta Lake version
ARG DELTA_LAKE_VERSION=3.3.0
ARG SCALA_VERSION=2.12

# Set a directory for custom JARs within the image
ENV DELTA_JARS_DIR=/opt/bitnami/spark/jars/delta

# Create the directory
RUN mkdir -p ${DELTA_JARS_DIR}

# Download Delta Lake JARs directly from Maven Central using curl
# -sL: silent (no progress bar), follow redirects
# -o: output file name
RUN curl -sL https://repo1.maven.org/maven2/io/delta/delta-spark_${SCALA_VERSION}/${DELTA_LAKE_VERSION}/delta-spark_${SCALA_VERSION}-${DELTA_LAKE_VERSION}.jar -o ${DELTA_JARS_DIR}/delta-spark_${SCALA_VERSION}-${DELTA_LAKE_VERSION}.jar && \
    curl -sL https://repo1.maven.org/maven2/io/delta/delta-storage/${DELTA_LAKE_VERSION}/delta-storage-${DELTA_LAKE_VERSION}.jar -o ${DELTA_JARS_DIR}/delta-storage-${DELTA_LAKE_VERSION}.jar

# The SPARK_DRIVER_CLASS_PATH and SPARK_EXECUTOR_EXTRA_CLASSPATH will be set in docker-compose.yml
# to point to ${DELTA_JARS_DIR}/*