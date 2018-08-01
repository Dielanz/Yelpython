
#This file is a throwaway, but it basically shows that the restaurant attributes file is not very useful

import pandas as pd
import numpy as np

pd.set_option('display.max_rows', 500)

yelp_restaurants = pd.read_csv('yelp_restaurants.csv')

yelp_attributes = pd.read_csv('yelp_business_attributes.csv')

yelp_rest_attrib = pd.merge(yelp_restaurants, yelp_attributes, how = 'left', on = 'business_id')

#https://stackoverflow.com/questions/34794067/how-to-set-a-cell-to-nan-in-a-pandas-dataframe

yelp_rest_attrib = yelp_rest_attrib.replace('Na',np.NaN)

yelp_rest_attrib.count()

yelp_rest_attrib[yelp_rest_attrib['review_count']>10]

