import unittest
import pandas as pd
from SystemCleanup import SystemCleanup

class TestOperations(unittest.TestCase):

    def test_nullsremoved(self):
        rowsToTest = pd.DataFrame({
            "Books": ["Dracula", None, None,None,"Bible",None,None],
            "Customer ID": [1, None, 3,None,4,5,None],
        })
        cleanedRows = SystemCleanup.removeNullRows(rowsToTest)
        self.assertEqual(cleanedRows.index.tolist(),[0,2,4,5],"Expected only fully empty rows to be removed")
    
    def test_convertWeeksToDays(self):
        weeksToTest = pd.Series(["1 week", "2 weeks", "3 weeks", "12 weeks"])
        expected = pd.Series([7,14,21,84])
        calcDays = SystemCleanup.convertWeeksToDays(weeksToTest)
        self.assertEqual(calcDays.tolist(), expected.tolist(),"Incorrect number of days")

    def test_quotesremoved(self):
        datesToTest = pd.Series(['"01/06/2027"', '"05/10/1990"', "01/06/2022"])
        expected = ["01/06/2027", "05/10/1990", "01/06/2022"]
        cleanedDates = SystemCleanup.removeQuotes(datesToTest)
        self.assertEqual(cleanedDates.tolist(),expected,"Quotes not removed from dates")

    def test_convertToInt(self):
        numericsToTest = pd.Series([1.0,3.0,4.0,5.0])
        convertedInts = SystemCleanup.convertToInt(numericsToTest)
        self.assertEqual(str(convertedInts.dtype),"Int64","Numerics not converted to int")

if __name__ == "__main__":
    unittest.main()