class SystemCleanup: 

    @staticmethod
    def removeNullRows(sb):
        sb = sb.dropna(how="all")
        return sb
    
    @staticmethod    
    def convertWeeksToDays(weekVal):
        return weekVal.str.extract(r"(\d+)", expand=False).astype("Int64") * 7 
    
    @staticmethod
    def removeQuotes(sb):
        sb=sb.str.strip('"')
        return sb
    
    @staticmethod 
    def convertToInt(sb):
        return sb.astype("Int64")