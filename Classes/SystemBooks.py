import pandas as pd 

class SystemBooks: 
    def __init__(self,systemBooks):
        self.systemBooks = systemBooks
    
    def cleanBooks(self):
    
        # Remove nulls / Nan
        sb = self.systemBooks.dropna(how="all")
    
        # Strip the '"" from dates
        sb["Book checkout"] = sb["Book checkout"].str.strip('"')
        
        # Convert IDs to int 
        sb["Customer ID"] = sb["Customer ID"].astype("Int64")
        sb["Id"] = sb["Id"].astype("Int64")
        
        # Convert weeks to days 
        sb["Days allowed to borrow"] = sb["Days allowed to borrow"].str.extract(r"(\d+)", expand=False).astype("Int64") * 7 

        self.systemBooks = sb
    
    def validateBooks(self): 

        sb = self.systemBooks

        # Check for empty book names
        sb["Valid Rows"] = "Pass"
        sb["Valid Rows"] = sb["Valid Rows"].mask(sb["Books"].isna(), "Fail - invalid book name")    
        
        # Convert to datetime + remove invalid dates 
        for c in ["Book checkout", "Book Returned"]:
            sb[c] = pd.to_datetime(sb[c], format="%d/%m/%Y", errors="coerce")
    
        # Invalid date
        sb["Valid Rows"] = sb["Valid Rows"].mask(sb["Book checkout"].isna() | sb["Book Returned"].isna(), "Fail - invalid date")
    
        # Book checkout >= Book Returned
        sb["Valid Rows"] = sb["Valid Rows"].mask(sb["Book checkout"] >= sb["Book Returned"], "Fail - checkout not before return")
    
        # The checkout date or return is in the future
        sb["Valid Rows"] = sb["Valid Rows"].mask((sb["Book checkout"] > pd.Timestamp.today()) | (sb["Book Returned"] > pd.Timestamp.today()), "Fail - future date")
    
        self.systemBooks = sb
