import argparse
import pandas as pd

from Classes.SystemBooks import SystemBooks
from Classes.SystemCustomers import SystemCustomers
from Classes.OutputData import DataOutputHandle

def parseArgs():
    parser = argparse.ArgumentParser(description="Clean and validate library data")
    parser.add_argument("--db",action="store_true",help="Save to the database instead of a local file")
    return parser.parse_args()

def main():

    args = parseArgs()

    print("\nPulling local files...\n")  

    # # Pull the data 
    systembook = SystemBooks(pd.read_csv("data/03_Library Systembook.csv"))
    systemCustomers = SystemCustomers(pd.read_csv("data/03_Library SystemCustomers.csv"))

    print(f"Validating {len(systembook.systemBooks)} Books...")
    print(f"Validating {len(systemCustomers.systemCustomers)} Customers...\n")

    # Sort the Books 
    systembook.cleanBooks()
    systembook.validateBooks()

    # Sort the Customers
    systemCustomers.cleanAndValidateCustomers()

    print(f"Validated! {len(systembook.systemBooks[systembook.systemBooks["Valid Rows"] == "Pass"])} Books remain...")
    print(f"Validated! {len(systemCustomers.systemCustomers)} Customers remain...\n")

    if(args.db):
        print("Exporting to database...\n")
    else:
        print("Exporting to local files...\n")  

    # Output
    exportHandler = DataOutputHandle(systembook.systemBooks,systemCustomers.systemCustomers)
    exportHandler.outputFiles(args.db)

    print("Completed without failure! Please check results...\n")  

if __name__ == "__main__":
    main()