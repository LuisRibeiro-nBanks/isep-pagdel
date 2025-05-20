FROM bitnami/spark:3.3.1

USER root

# Instalar dependências Python
RUN pip install --no-cache-dir \
    delta-spark==2.3.0 \
    kafka-python

# Definir variáveis de ambiente para PySpark
ENV PYSPARK_PYTHON=python3 \
    PYSPARK_DRIVER_PYTHON=python3
