# Group: yelPython
# Members: Ruslan Askerov (ra7kv), Will Daniel (wkd9th), Zach Lynch (zsl2gf), Le Michael Song (ls2ywj), Dylan Weber (dew2ad)

# Import libraries
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import wordcloud
from Vegas_functions import sumCategoryData
from nltk.sentiment.vader import SentimentIntensityAnalyzer

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

#####################################################################################
#####################################################################################
#####################################################################################
########################## Category Data Analysis ###################################

# Run the sumCategoryData
categoryList_Vegas = sumCategoryData(dfVegas_filtered)

categoryList_Vegas["AvgStars_distinct"] = categoryList_Vegas["avg_distinct_review"] / categoryList_Vegas["distinct_count"]
categoryList_Vegas["AvgStars_byReview"] = categoryList_Vegas["avg_weighted_review"] / categoryList_Vegas["review_count"]
categoryList_Vegas = categoryList_Vegas[categoryList_Vegas["name"] != "Food"]

# Filter out only categories that have at least 20 restauarant
dfVegas_sub = categoryList_Vegas[categoryList_Vegas["distinct_count"] > 20]

top_10 = dfVegas_sub.nlargest(10, 'AvgStars_byReview')
bottom_10 = dfVegas_sub.nsmallest(10, 'AvgStars_byReview')

# Formatting source: http://pbpython.com/effective-matplotlib.html
plt.style.use('seaborn')

# Get the figure and the axes
fig, (ax0, ax1) = plt.subplots(nrows=2,ncols=1, sharex=True, figsize=(6, 7))
top_10.plot(kind='barh', y="AvgStars_byReview", x="name", ax=ax0)
ax0.set_xlim([3, 5])
ax0.set(title='Top 10 Categories', xlabel='Avg Review', ylabel='Category')

# Plot the average as a vertical line
avg = categoryList_Vegas['AvgStars_byReview'].mean()
ax0.axvline(x=avg, color='b', label='Average', linestyle='--', linewidth=1)

# Get the figure and the axes
bottom_10.plot(kind='barh', y="AvgStars_byReview", x="name", ax=ax1)
ax1.set_xlim([3, 5])
ax1.set(title='Bottom 10 Categories', xlabel='Avg Review', ylabel='Category')
ax1.axvline(x=avg, color='b', label='Average', linestyle='--', linewidth=1)

# Title the figure
fig.suptitle('Vegas Reviews by Category', fontsize=14, fontweight='bold')

# Hide the legends
ax1.legend().set_visible(False)
ax0.legend().set_visible(False)

#####################################################################################
#####################################################################################
#####################################################################################
############################ Sentiment Analysis #####################################

#The following is based on the yelp_text_analysis file, but for Vegas data only 

sid = SentimentIntensityAnalyzer()

top = pd.DataFrame(dfVegasReview_filtered[dfVegasReview_filtered['stars'] == 5])
bot = pd.DataFrame(dfVegasReview_filtered[(dfVegasReview_filtered['stars'] == 1) | (dfVegasReview_filtered['stars'] == 1.5)])

top = top.sample(10000)
bot = bot.sample(10000)

#Defines a function that concatenates the item of a pd series into one string
# to create the wordcloud
def collectStrings(series):
    fullText = ''
    for txt in list(series):
        fullText += txt
    return fullText

#Create empty dictionary 
txt = {}

#Populate the dictionary with 5 star review text
txt.update({'top': collectStrings(top['text'])})

#Populate the dictionary with 1 star review text
txt.update({'bot': collectStrings(bot['text'])})

#Code to create the wordcloud
for key, val in txt.items():
    print(str(key) + ': ')
    wc = wordcloud.WordCloud(max_font_size=40).generate(val)
    plt.figure(figsize=(12,9), facecolor='w')
    plt.imshow(wc, interpolation="bilinear")
    plt.imshow(wc)
    plt.axis("off")
    plt.savefig(str(key) + '.png')
    plt.show()

#Create dataframes of users similar to the data used in the histograms above (1 review and more than 68)
high = pd.Series(dfVegasUser_filtered[dfVegasUser_filtered['review_count'] > 68].index)
low = pd.Series(dfVegasUser_filtered[dfVegasUser_filtered['review_count'] == 1].index)

#Split the two groups into four by adding the 5 star or 1 star dimension
highTop = top.loc[top.index.get_level_values(1).isin(high)]
highBot = bot.loc[bot.index.get_level_values(1).isin(high)]

lowTop = top.loc[top.index.get_level_values(1).isin(low)]
lowBot = bot.loc[bot.index.get_level_values(1).isin(low)]

#Get the mean compound polarity score for each group above (highTop, highBot, lowTop, lowBot)
pd.Series([x['compound'] for x in highTop['text'].apply(sid.polarity_scores)]).mean()
pd.Series([x['compound'] for x in highBot['text'].apply(sid.polarity_scores)]).mean()
pd.Series([x['compound'] for x in lowTop['text'].apply(sid.polarity_scores)]).mean()
pd.Series([x['compound'] for x in lowBot['text'].apply(sid.polarity_scores)]).mean()

#####################################################################################
#####################################################################################
#####################################################################################
############################ Correlation Analysis ###################################

#Create a list of distinct categories
categories_set = sorted(set([category for row in dfVegas_filtered['categories'] for category in row.split(';')]))

#Remove the category restaurant (all )
categories_set.remove('Restaurants')

#To be used with pandas.apply to create a new column for every category in categories_set
def createCategoryColumn(categories,category):
    category_list = categories.split(';')
    return 1 if category in category_list else np.NaN

#Create a new column for every category in categories_set
for category in categories_set:
    dfVegas_filtered[category] = dfVegas_filtered['categories'].apply(createCategoryColumn, category = category)

#Create a dataframe of counts of each category of each restaurant (hence the np.NaN rather then 0 above)
#Used reset index to make the categories a column again   
counts_by_category = pd.DataFrame(dfVegas_filtered.count()).reset_index()

#Rename the columns of the counts_by_category df
counts_by_category.columns = ['Category','Counts']

#Sort the df by Counts
counts_by_category.sort_values(by='Counts')

#To be used in testing
#counts_by_category.to_csv('test_corr_matrix.csv')

#For the correlation matrix, we use the most frequently occuring categories

# 96	Food	365 # remove
# 164	Nightlife	333 #Nightlife is no good bc it is a supercategory
# 29	Bars	325
# 16	American (Traditional)	278
# 15	American (New)	229
# 41	Breakfast & Brunch	208
# 132	Italian	164
# 198	Seafood	157
# 154	Mexican	154
# 180	Pizza	154
# 133	Japanese	147
# 195	Sandwiches	145
# 46	Burgers	128
# 60	Chinese	119
# 215	Sushi Bars	118
# 212	Steakhouses	116
# 23	Asian Fusion	115


#Replace NAs with zeros
dfVegas_filtered = dfVegas_filtered.replace(np.NaN,0)

#print(yelp_restaurants.columns.tolist())

#Rename stars and review_count to make the chart look a bit nicer
dfVegas_filtered = dfVegas_filtered.rename(columns={'stars':'Stars','review_count':'Review Count'})

desired_columns_list = ['American (Traditional)','Sandwiches','Bars','Pizza','Mexican','Burgers','American (New)','Breakfast & Brunch','Italian','Chinese','Steakhouses','Sushi Bars','Seafood','Asian Fusion','Stars','Review Count']

#Subset data on desired columns to then feed to the correlation matrix
dfVegas_filtered = dfVegas_filtered[desired_columns_list]

#https://stackoverflow.com/questions/29432629/correlation-matrix-using-pandas

#Creation of the heatmap (visualized correlation matrix)
import seaborn as sns
corr = dfVegas_filtered.corr()
sns.heatmap(corr, 
            xticklabels=corr.columns.values,
            yticklabels=corr.columns.values,
            vmin = -1.000, #set the scale from -1 to 1
            vmax = 1.000,
            cmap=sns.color_palette("coolwarm",1000)) #Create the color palette