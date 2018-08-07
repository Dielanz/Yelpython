
import pandas as pd
import numpy as np

#This is useful to see more data in a dataframe when printing it to the console
pd.set_option('display.max_rows', 10000)

#Read in cleaned data
yelp_restaurants = pd.read_csv('yelp_restaurants_CLEANED.csv')

#Create a list of distinct categories
categories_set = sorted(set([category for row in yelp_restaurants['categories'] for category in row.split(';')]))

#Remove the category restaurant (all )
categories_set.remove('Restaurants')

#To be used with pandas.apply to create a new column for every category in categories_set
def createCategoryColumn(categories,category):
    category_list = categories.split(';')
    return 1 if category in category_list else np.NaN

#Create a new column for every category in categories_set
for category in categories_set:
    yelp_restaurants[category] = yelp_restaurants['categories'].apply(createCategoryColumn, category = category)

#Create a dataframe of counts of each category of each restaurant (hence the np.NaN rather then 0 above)
#Used reset index to make the categories a column again   
counts_by_category = pd.DataFrame(yelp_restaurants.count()).reset_index()

#Rename the columns of the counts_by_category df
counts_by_category.columns = ['Category','Counts']

#Sort the df by Counts
counts_by_category.sort_values(by='Counts')

#To be used in testing
#counts_by_category.to_csv('test_corr_matrix.csv')

#For the correlation matrix, we use the most frequently occuring categories

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

#Replace NAs with zeros
yelp_restaurants = yelp_restaurants.replace(np.NaN,0)

#print(yelp_restaurants.columns.tolist())

#Rename stars and review_count to make the chart look a bit nicer
yelp_restaurants = yelp_restaurants.rename(columns={'stars':'Stars','review_count':'Review Count'})

desired_columns_list = ['American (Traditional)','Sandwiches','Bars','Pizza','Mexican','Burgers','American (New)','Breakfast & Brunch','Italian','Chinese','Salad','Chicken Wings','Seafood','Cafes','Sports Bars','Stars','Review Count']

#Subset data on desired columns to then feed to the correlation matrix
yelp_restaurants = yelp_restaurants[desired_columns_list]

#https://stackoverflow.com/questions/29432629/correlation-matrix-using-pandas

#Creation of the heatmap (visualized correlation matrix)
import seaborn as sns
corr = yelp_restaurants.corr()
sns.heatmap(corr, 
            xticklabels=corr.columns.values,
            yticklabels=corr.columns.values,
            vmin = -1.000, #set the scale from -1 to 1
            vmax = 1.000,
            cmap=sns.color_palette("coolwarm",1000)) #Create the color palette

