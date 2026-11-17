import pandas as pd

from Classes.SystemBooks import SystemBooks
from Classes.SystemCustomers import SystemCustomers
from Classes.dbConnect import SQLHelper

saveToDB = True

# Pull data 

def readCSV(url):
    return pd.read_csv(url)

def cleanupErrors(systembook):
    
    systembook = systembook[systembook["Valid Rows"] == "Pass"]
    systembook = systembook.drop(columns=["Valid Rows"])   
    return systembook

# Output 

def outputFiles(systembook,systemCustomers):

    import os

    # Move failed into seperate folder

    invalidRows_systembook = systembook[systembook["Valid Rows"] != "Pass"]

    # Cleanup failed + remove column

    systembook = cleanupErrors(systembook)

    os.makedirs("exportData", exist_ok=True)

    if(saveToDB):
        engine = SQLHelper.makeConnection()
        SQLHelper.saveInSQL(systembook,systemCustomers,invalidRows_systembook,engine)
    else:
        systembook.to_csv("exportData/systembook.csv", index=False)
        systemCustomers.to_csv("exportData/systemCustomers.csv", index=False)
        invalidRows_systembook.to_csv("exportData/systembook_invalidRows.csv", index=False)

# # Pull the data 

systembook = SystemBooks(readCSV("data/03_Library Systembook.csv"))
systemCustomers = SystemCustomers(readCSV("data/03_Library SystemCustomers.csv"))

# Sort the Books 

systembook.cleanBooks()
systembook.validateBooks()

# Sort the customers
systemCustomers.cleanAndValidateCustomers()

# Output
outputFiles(systembook.systemBooks,systemCustomers.systemCustomers)