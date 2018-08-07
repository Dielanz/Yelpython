from Vegas_functions import sumCategoryData
import unittest
import pandas as pd
import os

os.chdir("..")

# Pull in first row yelp_business        
dfYelp = pd.read_csv('yelp_restaurants_CLEANED.csv', index_col = ("business_id"))

dfTopTwoRows = dfYelp.iloc[0:2]

class test_sumCategoryData(unittest.TestCase):
    def test_categories_set_is_outputting_as_expected(self):
        dfTest = sumCategoryData(dfTopTwoRows)    
        testList = ['American (New)', 'American (Traditional)','Bars','Burgers','Nightlife','Salad','Sandwiches','Soup']
        print(dfTest["name"].tolist())
        self.assertEqual(dfTest["name"].tolist(), testList, msg = "List did not contain expected categories!")
        
    def test_categories_count_is_outputting_as_expected(self):
        dfTest = sumCategoryData(dfTopTwoRows)
        print(dfTest.loc[dfTest["name"]=="Sandwiches"]["distinct_count"].values[0])
        self.assertEqual(dfTest.loc[dfTest["name"]=="Sandwiches"]["distinct_count"].values[0], 2, msg = "Values are not adding up correctly")

if __name__ == '__main__':
    unittest.main()