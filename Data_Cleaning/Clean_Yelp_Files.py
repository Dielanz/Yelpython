# Group: yelPython
# Members: Ruslan Askerov (ra7kv), Will Daniel (wkd9th), Zach Lynch (zsl2gf), Le Michael Song (ls2ywj), Dylan Weber (dew2ad)


# the purpose of this file is to read through all our datafiles
# and clean them. We filter and remove restaurants that don't have
# population and income data, which means that they are not US based. We also
# filter out the closed businesses. And lastly we remove all the column
# that are unnecessary for our analysis

import pandas as pd
from collections import Counter

# INPUT - Read in the data files we will be using
# CSV Files needed in directory - yelp_business_new, yelp_business_hours, yelp_user, yelp_review, and columnNames
yelp_business = pd.read_csv('yelp_business_new.csv', index_col = 'business_id')
yelp_hours = pd.read_csv('yelp_business_hours.csv', index_col = 'business_id')
yelp_users = pd.read_csv('yelp_user.csv', index_col = "user_id")
yelp_reviews = pd.read_csv('yelp_review.csv', index_col = ("business_id","user_id"))
keepColumns = pd.read_csv("columnNames.csv") # Outputted and editted via "Create_ColumnNames_output.py"

## yelp_business > filter out any business is not a restaurant
list_cat = [category for row in yelp_business['categories'] for category in row.split(';')]

#https://stackoverflow.com/questions/2600191/how-to-count-the-occurrences-of-a-list-item
count_of_items = Counter(list_cat)

def summarize_dataframe(df):
    """Summarize a dataframe, and report missing values."""
    missing_values = pd.concat([pd.DataFrame(df.columns, columns=['Variable Name']), 
                      pd.DataFrame(df.dtypes.values.reshape([-1,1]), columns=['Data Type']),
                      pd.DataFrame(df.isnull().sum().values, columns=['Missing Values']), 
                      pd.DataFrame([df[name].nunique() for name in df.columns], columns=['Unique Values'])], 
                     axis=1).set_index('Variable Name')
    with pd.option_context("display.max_rows", 1000):
        display(pd.concat([missing_values, df.describe(include='all').transpose()], axis=1).fillna(""))


def isRestaurant(row):
    return 1 if 'Restaurants' in row.split(';') else 0

yelp_business['isRestaurant'] = yelp_business['categories'].apply(isRestaurant)

yelp_restaurants = yelp_business[yelp_business['isRestaurant']==1]

#Delete unnecessary column
del yelp_restaurants['isRestaurant']

# Filter out any restuarant where we don't have income data
yelp_restaurants = yelp_restaurants[pd.notnull(yelp_restaurants['pop_income'])]

# Filter out any restaurant that is closed
yelp_restaurants = yelp_restaurants[yelp_restaurants['is_open'] != 0]

### Drop the unneccessary columns we will not be using for all files
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

# Remove the columns and data that we don't want from each data set
yelp_restaurants = filterColumnsAndRows(yelp_restaurants, keepColumns, "yelp_business")
yelp_hours = filterColumnsAndRows(yelp_hours, keepColumns, "yelp_business_hours", yelp_restaurants)
yelp_reviews = filterColumnsAndRows(yelp_reviews, keepColumns, "yelp_review", yelp_restaurants)
yelp_users = filterColumnsAndRows(yelp_users, keepColumns, "yelp_user", yelp_reviews)

# Merge the yelp_hours with yelp_restaurants
yelp_rest_hours = pd.merge(yelp_restaurants, yelp_hours, left_index = True, right_index = True)

# OUTPUT - all three cleaned files
yelp_restaurants.to_csv('yelp_restaurants_CLEANED.csv')
yelp_users.to_csv('yelp_users_CLEANED.csv')
yelp_reviews.to_csv('yelp_reviews_CLEANED.csv')
