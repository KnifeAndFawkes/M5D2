import pandas as pd 
from pathlib import Path
import sqlite3

class SQLHelper: 

    @staticmethod
    def createTablesDef(systembook,systemCustomers,invalidRows_systembook): 
        tables = {
            "systembook": systembook,
            "systemCustomers": systemCustomers,
            "systembookErrors": invalidRows_systembook,
        }
        return tables

    @staticmethod
    def saveInSQL(systembook,systemCustomers,invalidRows_systembook): 

        # Generate Tables

        tables = SQLHelper.createTablesDef(systembook, systemCustomers, invalidRows_systembook)

        with sqlite3.connect("exportData/library.db") as conn:
            for name, df in tables.items():
                df.to_sql(name, conn, if_exists="replace", index=False)

        print("Database save complete...\n")

    @staticmethod
    def validateSQL(systembook,systemCustomers,invalidRows_systembook):
        validationResults = "Validating sql tables..."
        validationSuccess = True

        tables = SQLHelper.createTablesDef(systembook, systemCustomers, invalidRows_systembook)

        # Validate each table 

        with sqlite3.connect("exportData/library.db") as conn:
            for name, df in tables.items():
                # Get count from SQL
                rowcountsql = conn.execute(f"SELECT COUNT(1) FROM {name}").fetchone()[0]
                # Get actual count 
                rowcount = len(df)
                # Log result 
                validationResults += f"\n\nTable - {name}: sql rows = {rowcountsql}, actual rows = {rowcount}\n"
                # Check result 
                if rowcount != rowcountsql: 
                    validationResults += "Validation Failed! Incorrect row count"
                    validationSuccess = False
                else:
                    validationResults +=  "Validation Success! Correct row count"


        out = Path("exportData/SQLValidation.txt")
        
        with out.open("a") as f:
            f.write(validationResults)

        return validationSuccess

                