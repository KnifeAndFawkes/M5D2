import pandas as pd

from Classes.SystemBooks import SystemBooks
from Classes.SystemCustomers import SystemCustomers
from Classes.OutputData import DataOutputHandle

saveToDB = False

# # Pull the data 
systembook = SystemBooks(pd.read_csv("data/03_Library Systembook.csv"))
systemCustomers = SystemCustomers(pd.read_csv("data/03_Library SystemCustomers.csv"))

# Sort the Data 
systembook.cleanBooks()
systembook.validateBooks()
systemCustomers.cleanAndValidateCustomers()

# Output
exportHandler = DataOutputHandle(systembook.systemBooks,systemCustomers.systemCustomers)
exportHandler.outputFiles(saveToDB)