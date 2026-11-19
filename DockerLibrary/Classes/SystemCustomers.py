import pandas as pd 
from Classes.SystemCleanup import SystemCleanup

class SystemCustomers: 
    def __init__(self,systemCustomers):
        self.systemCustomers = systemCustomers
    
    # Customer Cleanup 

    def cleanAndValidateCustomers(self): 
        
        sc = self.systemCustomers
        
        sc= SystemCleanup.removeNullRows(sc)

        # Convert IDs to int 
        sc["Customer ID"] = SystemCleanup.convertToInt(sc["Customer ID"])

        self.systemCustomers = sc