#TODO: Add comments
#Filters the yelp_business csv to only restaurants, appends income data, and filters to non-missing income attribute

import pandas as pd
from collections import Counter

yelp_business = pd.read_csv('yelp_business_new.csv', index_col = ("business_id"))

list_cat = [category for row in yelp_business['categories'] for category in row.split(';')]

#https://stackoverflow.com/questions/2600191/how-to-count-the-occurrences-of-a-list-item
count_of_items = Counter(list_cat)

#https://stackoverflow.com/questions/11228812/print-a-dict-sorted-by-values
print(sorted( ((val, ki) for ki, val in count_of_items.items()), reverse=True))

def isRestaurant(row):
    return 1 if 'Restaurants' in row.split(';') else 0 

yelp_business['isRestaurant'] = yelp_business['categories'].apply(isRestaurant)

yelp_restaurants = yelp_business[(pd.notnull(yelp_business['pop_income'])) & (yelp_business['is_open'] != 0) & (yelp_business['isRestaurant']==1)]

yelp_restaurants = yelp_restaurants.drop(columns=['isRestaurant','neighborhood', 'address', 'Unnamed: 0'])

#yelp_restaurants.to_csv('yelp_restaurants.csv')

# Bring in yelp_business_attributes, and yelp_business hours to merge with yelp_restaurants

dfYelpAttributes = pd.read_csv('yelp_business_attributes.csv',
                               index_col = "business_id")

dfYelpHours = pd.read_csv('yelp_business_hours.csv',
                               index_col = "business_id")


