# Import libraries
import pandas as pd
import numpy as np

# Pull in yelp_business file
dfYelp = pd.read_csv('yelp_business.csv', index_col = "business_id")

dfVegas = dfYelp[dfYelp["city"] == "Las Vegas"]

dfVegas.set_index("business_id", inplace=True)

del dfYelp

# Pull in yelp_business_attributes file & filter down to just Vegas

dfYelpAttributes = pd.read_csv('yelp_business_attributes.csv',
                               index_col = "business_id")

dfVegasAttributes = dfYelpAttributes[dfYelpAttributes.index.isin(dfVegas.index)]
dfVegasNoAttributes = dfVegas[~dfVegas.index.isin(dfVegasAttributes.index)]

del dfYelpAttributes

# Pull in yelp_business_hours file & filter down to just Vegas

dfYelpHours = pd.read_csv('yelp_business_hours.csv',
                               index_col = "business_id")

dfVegasHours = dfYelpHours[dfYelpHours.index.isin(dfVegas.index)]

del dfYelpHours

# Pull in yelp_review file & filter down to just Vegas

dfYelpReview = pd.read_csv('yelp_review.csv',
                               index_col = "business_id")

dfVegasReview = dfYelpReview[dfYelpReview.index.isin(dfVegas.index)]

del dfYelpReview