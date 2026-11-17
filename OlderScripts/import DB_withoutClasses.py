import pandas as pd
import sqlalchemy as sql

saveToDB = True

server = "localhost"
database = "Library"

# Pull data 

def readCSV(url):
    return pd.read_csv(url)

# Book cleanup 

def cleanBooks(systembook):
    
    # Remove nulls / Nan
    systembook = systembook.dropna(how="all")

    # Strip the '"" from dates
    systembook["Book checkout"] = systembook["Book checkout"].str.strip('"')
    
    # Convert IDs to int 
    systembook["Customer ID"] = systembook["Customer ID"].astype("Int64")
    systembook["Id"] = systembook["Id"].astype("Int64")
    
    # Convert weeks to days 
    systembook["Days allowed to borrow"] = systembook["Days allowed to borrow"].str.extract(r"(\d+)", expand=False).astype("Int64") * 7 
    
    return systembook

def validateBooks(systembook): 

    # Check for empty book names
    systembook["Valid Rows"] = "Pass"
    systembook["Valid Rows"] = systembook["Valid Rows"].mask(systembook["Books"].isna(), "Fail - invalid book name")    
    
    # Convert to datetime + remove invalid dates 
    for c in ["Book checkout", "Book Returned"]:
        systembook[c] = pd.to_datetime(systembook[c], format="%d/%m/%Y", errors="coerce")

    # Invalid date
    systembook["Valid Rows"] = systembook["Valid Rows"].mask(systembook["Book checkout"].isna() | systembook["Book Returned"].isna(), "Fail - invalid date")

    # Book checkout >= Book Returned
    systembook["Valid Rows"] = systembook["Valid Rows"].mask(systembook["Book checkout"] >= systembook["Book Returned"], "Fail - checkout not before return")

    # The checkout date or return is in the future
    systembook["Valid Rows"] = systembook["Valid Rows"].mask((systembook["Book checkout"] > pd.Timestamp.today()) | (systembook["Book Returned"] > pd.Timestamp.today()), "Fail - future date")

    return systembook

def cleanupErrors(systembook):
    
    systembook = systembook[systembook["Valid Rows"] == "Pass"]
    systembook = systembook.drop(columns=["Valid Rows"])   
    return systembook

# Customer Cleanup 

def cleanAndValidateCustomers(systemCustomers): 

    # Remove empty or NAN rows 
    systemCustomers = systemCustomers.dropna(how="all")

    # Convert IDs to int 
    systemCustomers["Customer ID"] = systemCustomers["Customer ID"].astype("Int64")

    return systemCustomers

# Output 

def outputFiles(systembook,systemCustomers):

    import os

    # Move failed into seperate folder

    invalidRows_systembook = systembook[systembook["Valid Rows"] != "Pass"]

    # Cleanup failed + remove column

    systembook = cleanupErrors(systembook)

    os.makedirs("exportData", exist_ok=True)

    if(saveToDB):
        engine = makeConnection()
        systembook.to_sql("systembook", con=engine, if_exists="replace", index=False)
        systemCustomers.to_sql("systemCustomers", con=engine, if_exists="replace", index=False)
        invalidRows_systembook.to_sql("systembookErrors", con=engine, if_exists="replace", index=False)
    else:
        systembook.to_csv("exportData/systembook.csv", index=False)
        systemCustomers.to_csv("exportData/systemCustomers.csv", index=False)
        invalidRows_systembook.to_csv("exportData/systembook_invalidRows.csv", index=False)

def makeConnection():
    from sqlalchemy import create_engine
    from sqlalchemy.engine import URL


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
        print("Connected")

    return engine


# # Pull the data 

systembook = readCSV("data/03_Library Systembook.csv")
systemCustomers = readCSV("data/03_Library SystemCustomers.csv")

# Sort the Books 
systembook = cleanBooks(systembook)
systembook = validateBooks(systembook)

# Sort the customers
systemCustomers = cleanAndValidateCustomers(systemCustomers)

# Output
outputFiles(systembook,systemCustomers)