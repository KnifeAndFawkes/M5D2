import pandas as pd 

class SystemCustomers: 
    def __init__(self,systemCustomers):
        self.systemCustomers = systemCustomers
    
    # Customer Cleanup 

    def cleanAndValidateCustomers(self): 

        sc = self.systemCustomers.dropna(how="all")

        # Convert IDs to int 
        sc["Customer ID"] = sc["Customer ID"].astype("Int64")

        self.systemCustomers = sc