# connect_db.py
import psycopg2
from sqlalchemy import create_engine

class PostgresDBConnector:
    def __init__(self, db_name, user, password, host='localhost', port=5432):
        self.connection = psycopg2.connect(
            dbname=db_name,
            user=user,
            password=password,
            host=host,
            port=port
        )
        self.engine = create_engine(f'postgresql+psycopg2://{user}:{password}@{host}:{port}/{db_name}')

    def getConnector(self):
        return self.engine.connect()

    def getCursor(self):
        return self.connection.cursor()

    def commit(self):
        self.connection.commit()

    def closeConnection(self):
        self.connection.close()
