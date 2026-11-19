import unittest
import pandas as pd
from SystemBooksHelper import SystemBooksHelper

class TestOperations(unittest.TestCase):

    def test_addValidRows(self):
        rowsToTest = pd.DataFrame({
            "Books": ["Dracula", None, None,None,"Bible",None,None],
            "Customer ID": [1, None, 3,None,4,5,None],
        })
        sb = SystemBooksHelper.addValidRows(rowsToTest)
        self.assertIn("Valid Rows",sb.columns,"Valid Rows column not added into list")
        self.assertTrue((sb["Valid Rows"] == "Pass").all(), "Not all rows contain Pass")

    def test_validateEmptyBookNames(self):
        rowsToTest = pd.DataFrame({
            "Books": ["Dracula", None, None,"Bible","Animal Farm"],
            "Customer ID": [1, 2, 3,4,5],
        })
        rowsToTest = SystemBooksHelper.addValidRows(rowsToTest)
        sb = SystemBooksHelper.validateEmptyBookNames(rowsToTest)
        sb = SystemBooksHelper.removeFailedRows(sb)
        self.assertEqual(sb.index.tolist(),[0,3,4],"Incorrect rows removed on book name validation")

    def test_datetimesConvert(self):
        rowsToTest = pd.DataFrame({
            "Book checkout": ["01/06/2020", "05/10/2021", "01/06/2022"],
            "Book Returned": ["01/06/2027", "05/10/1990", "01/06/2022"],
        })
        sb = SystemBooksHelper.convertDatetimes(rowsToTest)
        for c in ["Book checkout", "Book Returned"]:
            self.assertTrue(pd.api.types.is_datetime64_any_dtype(sb[c]), f"{c} failed to convert to datetime")

    def test_removeFailedRows(self):
        rowsToTest = pd.DataFrame({
            "Books": ["Dracula", None, None,"Bible","Animal Farm"],
            "Customer ID": [1, 2, 3,4,5],
            "Valid Rows": ["Pass","Pass","Fail","Pass","Fail"]
        })
        sb = SystemBooksHelper.removeFailedRows(rowsToTest)
        self.assertEqual(sb.index.tolist(),[0,1,3],"Incorrect fail rows removed")


if __name__ == "__main__":
    unittest.main()