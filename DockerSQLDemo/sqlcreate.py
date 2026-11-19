import sqlite3
from datetime import datetime

# Build Scripts 

dbPath = "/data/calcresults.db"

sqlCreateTable = "CREATE TABLE IF NOT EXISTS results (id INTEGER PRIMARY KEY, calculation VARCHAR(100), result NUMERIC(18,2), created DATETIME)"
sqlInsert = "INSERT OR REPLACE INTO results (id, calculation, result, created) "
sqlInsertVal1 = f"VALUES (1,'127/12',10.58,'{datetime.now()}')"
sqlInsertVal2 = f",(2,'12*12',144,'{datetime.now()}')"

# if __name__ == "__main__":
#     print(finalExec)

# Build DB if not exists and connect
with sqlite3.connect(dbPath) as conn:
    conn.execute(sqlCreateTable)
    conn.execute(sqlInsert + sqlInsertVal1 + sqlInsertVal2)
    conn.commit()
