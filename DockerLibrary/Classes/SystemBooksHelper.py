import pandas as pd 

class SystemBooksHelper: 
    def __init__(self,systemBooks):
        self.systemBooks = systemBooks

    @staticmethod
    def addValidRows(sb): 
        sb["Valid Rows"] = "Pass"
        return sb
    
    @staticmethod 
    def validateEmptyBookNames(sb):
        sb["Valid Rows"] = sb["Valid Rows"].mask(sb["Books"].isna(), "Fail - invalid book name") 
        return sb

    @staticmethod
    def convertDatetimes(sb):
        for c in ["Book checkout", "Book Returned"]:
            sb[c] = pd.to_datetime(sb[c], format="%d/%m/%Y", errors="coerce")
        return sb
    
    @staticmethod 
    def removeFailedRows(sb):        
        sb = sb[sb["Valid Rows"] == "Pass"]
        sb = sb.drop(columns=["Valid Rows"])   
        return sb