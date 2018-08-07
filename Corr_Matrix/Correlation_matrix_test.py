
#Unit testing the correlation matrix logic to get counts by category

import pandas as pd
from collections import Counter
import unittest

#Defining the class that inherits from unittest.TestCase
class testCorrMatrix(unittest.TestCase):

    #The unit test
    def test_validateCounts(self):
        #Input to correlation matrix created from Create_correlation_matrix.py file
        counts_by_category = pd.read_csv('test_corr_matrix.csv')

        #Filter to categories only
        counts_by_category = counts_by_category[counts_by_category['Counts']<20945]

        #Read in dataset to be validated against    
        yelp_restaurants = pd.read_csv('yelp_restaurants_CLEANED.csv')['categories'].tolist()

        #Create raw list of every appearance of every category
        list_categories = [y for x in yelp_restaurants for y in x.split(';')]
        
        #Create a Counter object from the list_categories object
        list_categories_counts = Counter(list_categories)

        #Used in unit test below to create a test column in the dataframe
        def getCount(category):
            return list_categories_counts[category]

        #Create the test column
        counts_by_category['Counts_test'] = counts_by_category['Category'].apply(getCount)

        #If the sum is greater than 0 the test fails (meaning at least 1 category count does not match)
        TestValue = sum(1 for x in counts_by_category['Counts_test'] == counts_by_category['Counts'] if x == False)
        
        #Tests that we get the same counts in the correlation matrix code as we do here in the unit test
        self.assertEqual(TestValue,0,msg='The validation counts do not match the test counts')

if __name__ == '__main__':
    unittest.main()


