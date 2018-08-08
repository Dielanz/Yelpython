# Group: yelPython
# Members: Ruslan Askerov (ra7kv), Will Daniel (wkd9th), Zach Lynch (zsl2gf), Le Michael Song (ls2ywj), Dylan Weber (dew2ad)

# Used in Vegas_Analysis to sum occurrences of restaurant categories in yelp_business_CLEANED dataset and a few other calculations

import pandas as pd

def sumCategoryData(dataframe):    
    # Find the category column in the data frame and create a list of all distinct categories
    categories_set = sorted(set([category for row in dataframe['categories'] for category in row.split(';')]))
    categories_set.remove('Restaurants') # We don't want "Restaurants" since everything is a restaurant

    # Set up our dataframe with the needed columns
    categoryList = pd.DataFrame(categories_set, columns=["name"])
    categoryList["avg_distinct_review"] = 0
    categoryList["avg_weighted_review"] = 0
    categoryList["review_count"] = 0
    categoryList["distinct_count"] = 0

    # Since this will be fed in through apply, this is executed on a per Row basis
    for index, row in dataframe.iterrows():
        rowCategoryList = row['categories'].split(';')
        for category in rowCategoryList:
            categoryList.loc[lambda x: x['name'] == category,["review_count","distinct_count","avg_distinct_review","avg_weighted_review"]] += (row["review_count"],1, row["stars"], row["stars"]*row["review_count"])
        
    return categoryList