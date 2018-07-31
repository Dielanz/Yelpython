import pandas as pd
from collections import Counter

# INPUT - Read in the data files we will be using
yelp_business = pd.read_csv('yelp_business_new.csv', index_col = 'business_id')
yelp_hours = pd.read_csv('yelp_business_hours.csv', index_col = 'business_id')
yelp_users = pd.read_csv('yelp_user.csv', index_col = "user_id")
yelp_reviews = pd.read_csv('yelp_review.csv', index_col = ("business_id","user_id"))

## yelp_business > filter out any business is not a restaurant

list_cat = [category for row in yelp_business['categories'] for category in row.split(';')]

#https://stackoverflow.com/questions/2600191/how-to-count-the-occurrences-of-a-list-item
count_of_items = Counter(list_cat)

def isRestaurant(row):
    return 1 if 'Restaurants' in row.split(';') else 0 

yelp_business['isRestaurant'] = yelp_business['categories'].apply(isRestaurant)

yelp_restaurants = yelp_business[yelp_business['isRestaurant']==1]

del yelp_restaurants['isRestaurant']

# Filter out any restuarant where we don't have income data
yelp_restaurants = yelp_restaurants[pd.notnull(yelp_restaurants['pop_income'])]

# Filter out any restaurant that is closed
yelp_restaurants = yelp_restaurants[yelp_restaurants['is_open'] != 0]

## Filter out those business from the business_hours, user, and review data as well

yelp_hours = yelp_hours[yelp_hours.index.isin(yelp_restaurants.index)]
yelp_reviews = yelp_reviews[yelp_reviews.index.get_level_values('business_id').isin(yelp_restaurants.index)]
yelp_users = yelp_users[yelp_users.index.isin(yelp_reviews.index.get_level_values("user_id"))]

### Drop the unneccessary columns we will not be using for all files

keepColumns = pd.read_csv("columnNames.csv") # Outputted and editted via "Create_ColumnNames_output.py"

# Remove restaurant columns we don't want
restaurantColumns = keepColumns[(keepColumns['file'] == "yelp_business") & keepColumns['keep']]
yelp_restaurants = yelp_restaurants[restaurantColumns["columnName"]]

# Remove hours columns we don't want
hoursColumns = keepColumns[(keepColumns['file'] == "yelp_business_hours") & keepColumns['keep']]
yelp_hours = yelp_hours[hoursColumns["columnName"]]

# Remove user columns we don't want
userColumns = keepColumns[(keepColumns['file'] == "yelp_user") & keepColumns['keep']]
yelp_users = yelp_users[userColumns["columnName"]]

# Remove review columns we don't want
reviewColumns = keepColumns[(keepColumns['file'] == "yelp_review") & keepColumns['keep']]
yelp_reviews = yelp_reviews[reviewColumns["columnName"]]

# Merge the yelp_hours with yelp_restaurants

yelp_rest_hours = pd.merge(yelp_restaurants, yelp_hours, left_index = True, right_index = True)

# OUTPUT - all three cleaned files
yelp_restaurants.to_csv('yelp_restaurants_CLEANED.csv')
yelp_users.to_csv('yelp_users_CLEANED.csv')
yelp_reviews.to_csv('yelp_reviews_CLEANED.csv')