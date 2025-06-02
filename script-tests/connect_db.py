import pandas as pd
import psycopg2
from sqlalchemy import create_engine
import sqlite3

def connect_db():
    
    # Database Credentials -> Alterar esta com as minhas configurações locais
    user = "isep-pagdel"
    password = "********"
    host = "localhost"
    port = "5432"
    database = "Air-Quality-Traffic"
    engine = create_engine(f"postgresql+psycopg2://{user}:{password}@{host}:{port}/{database}")
    
    
    return engine


# Não utilizem esta parte, foi só para testar a base de dados no meu PC da empresa.
# Só tinha o SQLite 
class TestDBConnector():
    def __init__(self, DB_file):

        # Connect to database
        self.conn = None

        # Create Cursor
        self.cursor = None
        
        self.DB_file = DB_file
        
        self.openConnection()
        

    def openConnection(self):
        self.conn = sqlite3.connect(self.DB_file)
        self.cursor = self.conn.cursor()

    def closeConnection(self):
        self.conn.close()

    def createCursor(self):
        self.cur=self.conn.cursor()
        
    def getConnector(self):
        return self.conn
    
    def getCursor(self):
        return self.cursor
