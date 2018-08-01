
import pandas as pd
import numpy as np

pd.set_option('display.max_rows', 10000)

yelp_restaurants = pd.read_csv('yelp_restaurants_CLEANED.csv')

categories_set = sorted(set([category for row in yelp_restaurants['categories'] for category in row.split(';')]))

categories_set.remove('Restaurants')

def createCategoryColumn(categories,category):
    category_list = categories.split(';')
    return 1 if category in category_list else np.NaN

for category in categories_set:
    yelp_restaurants[category] = yelp_restaurants['categories'].apply(createCategoryColumn, category = category)

counts_by_category = pd.DataFrame(yelp_restaurants.count()).reset_index()

counts_by_category.columns = ['Category','Counts']

counts_by_category.sort_values(by='Counts')

#539                              Thai     386
#500                              Soup     394
#538                           Tex-Mex     424
#63                           Bakeries     479
#507                    Specialty Food     483
#367                     Mediterranean     490
#449                              Pubs     492
#181                          Desserts     563
#183                            Diners     590
#68                           Barbeque     596
#50                       Asian Fusion     606
#520                        Sushi Bars     616
#515                       Steakhouses     637
#317                          Japanese     690
#124                          Caterers     692
#142                      Coffee & Tea     751
#178                             Delis     800
#510                       Sports Bars     809
#111                             Cafes     833
#476                           Seafood     984
#207         Event Planning & Services     999
#131                     Chicken Wings    1250
#470                             Salad    1262
#132                           Chinese    1381
#315                           Italian    1662
#97                 Breakfast & Brunch    2067
#31                     American (New)    2267
#105                           Burgers    2350
#369                           Mexican    2445
#429                             Pizza    3019
#70                               Bars    3195
#385                         Nightlife    3278 #Nightlife is no good bc it is a supercategory
#472                        Sandwiches    3398
#32             American (Traditional)    3460
#214                         Fast Food    3822

yelp_restaurants = yelp_restaurants.replace(np.NaN,0)

print(yelp_restaurants.columns.tolist())

desired_columns_list = ['American (Traditional)','Sandwiches','Bars','Pizza','Mexican','Burgers','American (New)','Breakfast & Brunch','Italian','Chinese','Salad','Chicken Wings','Seafood','Cafes','Sports Bars','stars','review_count']

yelp_restaurants = yelp_restaurants[desired_columns_list]

#https://stackoverflow.com/questions/29432629/correlation-matrix-using-pandas

#IN PROGRESS:

import seaborn as sns
corr = yelp_restaurants.corr()
sns.heatmap(corr, 
            xticklabels=corr.columns.values,
            yticklabels=corr.columns.values,
            vmin = -1.000,
            vmax = 1.000,
            cmap=sns.color_palette("coolwarm",1000))

