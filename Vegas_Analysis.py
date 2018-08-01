# Import libraries
import pandas as pd
import numpy as np

# Pull in yelp_business file
dfYelp = pd.read_csv('yelp_restaurants_CLEANED.csv', index_col = ("business_id"))

dfVegas = dfYelp[dfYelp["city"] == "Las Vegas"]

del dfYelp

# Pull in yelp_review file & filter down to just Vegas

dfYelpReview = pd.read_csv('yelp_reviews_CLEANED.csv',
                               index_col = ("business_id","user_id"))

dfVegasReview = dfYelpReview[dfYelpReview.index.get_level_values('business_id').isin(dfVegas.index)]

del dfYelpReview

# Pull in yelp_user file & filter down to just Vegas

dfYelpUser = pd.read_csv('yelp_users_CLEANED.csv',
                               index_col = "user_id")

dfVegasUser = dfYelpUser[dfYelpUser.index.isin(dfVegasReview.index.get_level_values("user_id"))]

del dfYelpUser


dfVegas_filtered = dfVegas[dfVegas["review_count"] > 100]
dfVegasReview_filtered = dfVegasReview[dfVegasReview.index.get_level_values('business_id').isin(dfVegas_filtered.index)]
dfVegasUser_filtered = dfVegasUser[dfVegasUser.index.isin(dfVegasReview_filtered.index.get_level_values("user_id"))]