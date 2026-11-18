import pandas as pd 
import os
from Classes.DBConnect import SQLHelper
from Classes.SystemBooksHelper import SystemBooksHelper

class DataOutputHandle: 

    def __init__(self,systembook,systemCustomers):
        self.systemCustomers = systemCustomers
        self.systembooks = systembook
        
    def outputFiles(self, saveToDB):
        
        sb = self.systembooks
        sc = self.systemCustomers

        # Move failed into seperate folder

        invalidRows_systembook = sb[sb["Valid Rows"] != "Pass"]

        # Cleanup failed + remove column
        sb = SystemBooksHelper.removeFailedRows(sb)

        os.makedirs("exportData", exist_ok=True)

        if(saveToDB):
            engine = SQLHelper.makeConnection()
            SQLHelper.saveInSQL(sb,sc,invalidRows_systembook,engine)
        else:
            sb.to_csv("exportData/systembook.csv", index=False)
            sc.to_csv("exportData/systemCustomers.csv", index=False)
            invalidRows_systembook.to_csv("exportData/systembook_invalidRows.csv", index=False)