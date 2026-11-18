import pandas as pd 
from Classes.SystemCleanup import SystemCleanup
from Classes.SystemBooksHelper import SystemBooksHelper

class SystemBooks: 
    def __init__(self,systemBooks):
        self.systemBooks = systemBooks

    def cleanBooks(self):
    
        sb = self.systemBooks

        # Remove nulls 
        sb= SystemCleanup.removeNullRows(sb)
    
        # Strip the '"" from dates
        sb["Book checkout"] = SystemCleanup.removeQuotes(sb["Book checkout"])
        
        # Convert IDs to int 
        sb["Customer ID"] = SystemCleanup.convertToInt(sb["Customer ID"])
        sb["Id"] = SystemCleanup.convertToInt(sb["Id"])        
        
        # Convert weeks to days
        sb["Days allowed to borrow"] = SystemCleanup.convertWeeksToDays(sb["Days allowed to borrow"])

        self.systemBooks = sb    
    
    def validateBooks(self): 

        sb = self.systemBooks

        # Add new "valid" column
        sb = SystemBooksHelper.addValidRows(sb)

        # Check for empty book names
        sb = SystemBooksHelper.validateEmptyBookNames(sb) 
        
        # Convert to datetime + remove invalid dates 
        sb = SystemBooksHelper.convertDatetimes(sb)
    
        # Invalid date
        sb["Valid Rows"] = sb["Valid Rows"].mask(sb["Book checkout"].isna() | sb["Book Returned"].isna(), "Fail - invalid date")
    
        # Book checkout >= Book Returned
        sb["Valid Rows"] = sb["Valid Rows"].mask(sb["Book checkout"] >= sb["Book Returned"], "Fail - checkout not before return")
    
        # The checkout date or return is in the future
        sb["Valid Rows"] = sb["Valid Rows"].mask((sb["Book checkout"] > pd.Timestamp.today()) | (sb["Book Returned"] > pd.Timestamp.today()), "Fail - future date")
    
        self.systemBooks = sb
