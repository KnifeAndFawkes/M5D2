import pandas as pd 
import sqlalchemy as sql
from sqlalchemy import create_engine
from sqlalchemy.engine import URL

server = "localhost"
database = "Library"

class SQLHelper: 
        
    def makeConnection():

        url = URL.create(
            "mssql+pyodbc",
            host=server,
            database=database,
            query={
                "driver":"ODBC Driver 17 for SQL Server",
                "trusted_connection": "yes",
                "Encrypt":"yes",
                "TrustServerCertificate":"yes"
            }
        )

        engine = create_engine(url,fast_executemany=True)

        with engine.connect() as conn:
            print(f"Connected to database: {server}:{database}...\n")

        return engine
    
    def saveInSQL(systembook,systemCustomers,invalidRows_systembook, engine): 
        systembook.to_sql("systembook", con=engine, if_exists="replace", index=False)
        systemCustomers.to_sql("systemCustomers", con=engine, if_exists="replace", index=False)
        invalidRows_systembook.to_sql("systembookErrors", con=engine, if_exists="replace", index=False)
        print("Database save complete...\n")