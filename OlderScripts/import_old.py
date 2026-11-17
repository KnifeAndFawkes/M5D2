import pandas as pd

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
    
    systembook.to_csv("exportData/systembook.csv", index=False)
    systemCustomers.to_csv("exportData/systemCustomers.csv", index=False)
    invalidRows_systembook.to_csv("exportData/systembook_invalidRows.csv", index=False)

# Pull the data 

systembook = readCSV("data/03_Library Systembook.csv")
systemCustomers = readCSV("data/03_Library SystemCustomers.csv")

# Sort the Books 

systembook = cleanBooks(systembook)
systembook = validateBooks(systembook)

# Sort the customers

systemCustomers = cleanAndValidateCustomers(systemCustomers)

# Output

outputFiles(systembook,systemCustomers)