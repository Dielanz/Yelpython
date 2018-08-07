import pandas as pd
import unittest
import os

os.chdir("..")

### Bring over filterColumnsAndRows from Clean_Yelp_Files.py
def filterColumnsAndRows(dataframe, dfColumns, filetype, dfToFilterBy=None):
    '''
    This function is responsible for removing the specified columns and rows that we do not want in the data set
    The non-needed columns are in the keepColumns dataframe
    For data rows, we use indexing to remove the rows where that do not have a replicate index in the specified dataframe
    '''
    # Create filter columns using filetype input & columns set to true in keep column of dfColumns input file
    filterColumns = dfColumns[(dfColumns['file'] == filetype) & dfColumns['keep']]

    if dfToFilterBy is None:  # If we are not given another dataframe to filter by, just filter the columns
        return dataframe[filterColumns["columnName"]]
    elif isinstance(dataframe.index, pd.core.index.MultiIndex): #If input dataframe is multi-indexed, just filter by first index
        return dataframe.loc[dataframe.index.get_level_values(0).isin(dfToFilterBy.index),filterColumns["columnName"]]
    elif isinstance(dfToFilterBy.index, pd.core.index.MultiIndex): #If the dataframe frame to index by is multi-indexed, filter by its' second index
        return dataframe.loc[dataframe.index.isin(dfToFilterBy.index.get_level_values(1)),filterColumns["columnName"]]
    else:
        return dataframe.loc[dataframe.index.isin(dfToFilterBy.index),filterColumns["columnName"]]

class test_filterColumnsAndRows(unittest.TestCase):
    def test_filter_on_columns_works_correctly(self):
        ### Download the necessary csvs 
        yelp_business = pd.read_csv('yelp_business_new.csv', index_col = 'business_id')
        
        # Import columnName csv that should keep just the 'Name Column'
        keepColumns = pd.read_csv("columnNames_test.csv") 
        
        # Run filter columns and rows, but we are expecting just one column... "name"
        yelp_business = filterColumnsAndRows(yelp_business, keepColumns, "yelp_business")
        
        print(yelp_business.columns.tolist())
        # Run assert statement
        self.assertEqual(yelp_business.columns.tolist(), ['name'], msg = "Column names contains more than name")
        
    def test_filter_on_rows_from_business_works(self):
        ### Download the necessary csvs yelp_business_new
        yelp_business = pd.read_csv('yelp_business_new.csv', index_col = 'business_id')
        yelp_reviews = pd.read_csv('yelp_reviews.csv', index_col = ("business_id","user_id"))
        
        # Import columnName csv that should keep just the 'Name Column'
        keepColumns = pd.read_csv("columnNames_test.csv") 
        
        # Take top 3 rows from yelp_business & then run function to confirm reviews only shows those values
        yelp_business = yelp_business.head(3)
        
        # Run filterColumnsAndRows
        yelp_reviews = filterColumnsAndRows(yelp_reviews, keepColumns, "yelp_review", yelp_business)
        expectedList = sorted(yelp_business.index.tolist())
        
        print(sorted(list(set(yelp_reviews.index.get_level_values(0)))))
        
        # Check yelp reviews to make sure the only business_ids in the dataset are the ones from expected list above
        self.assertEqual(sorted(list(set(yelp_reviews.index.get_level_values(0)))), expectedList, msg = "Indexes in review and business don't match up")

if __name__ == '__main__':
    unittest.main()