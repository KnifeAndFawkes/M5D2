import pandas as pd
from Classes.SystemBooks import SystemBooks

# Pull data 

def readCSV(url):
    return pd.read_csv(url)

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
    systembook.cleanupErrors
    os.makedirs("exportData", exist_ok=True)
   
    systembook.to_csv("exportData/systembook.csv", index=False)
    systemCustomers.to_csv("exportData/systemCustomers.csv", index=False)
    invalidRows_systembook.to_csv("exportData/systembook_invalidRows.csv", index=False)

# Pull the data 

systembook = SystemBooks(readCSV("data/03_Library Systembook.csv"))
systemCustomers = readCSV("data/03_Library SystemCustomers.csv")

# Sort the Books 

systembook.cleanBooks()
systembook.validateBooks()

# Sort the customers

systemCustomers = cleanAndValidateCustomers(systemCustomers)

# Output

outputFiles(systembook,systemCustomers)