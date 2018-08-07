# Import libraries
import pandas as pd
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

sid = SentimentIntensityAnalyzer()

top = pd.DataFrame(dfVegasReview_filtered[dfVegasReview_filtered['stars'] == 5])
bot = pd.DataFrame(dfVegasReview_filtered[(dfVegasReview_filtered['stars'] == 1) | (dfVegasReview_filtered['stars'] == 1.5)])

top = top.sample(10000)
bot = bot.sample(10000)

def collectStrings(series):
    fullText = ''
    for txt in list(series):
        fullText += txt
    return fullText

txt = {}
txt.update({'top': collectStrings(top['text'])})
txt.update({'bot': collectStrings(bot['text'])})
for key, val in txt.items():
    print(str(key) + ': ')
    wc = wordcloud.WordCloud(max_font_size=40).generate(val)
    plt.figure(figsize=(12,9), facecolor='w')
    plt.imshow(wc, interpolation="bilinear")
    plt.imshow(wc)
    plt.axis("off")
    plt.savefig(str(key) + '.png')
    plt.show()

high = pd.Series(dfVegasUser_filtered[dfVegasUser_filtered['review_count'] > 68].index)
low = pd.Series(dfVegasUser_filtered[dfVegasUser_filtered['review_count'] == 1].index)

highTop = top.loc[top.index.get_level_values(1).isin(high)]
highBot = bot.loc[bot.index.get_level_values(1).isin(high)]

lowTop = top.loc[top.index.get_level_values(1).isin(low)]
lowBot = bot.loc[bot.index.get_level_values(1).isin(low)]

pd.Series([x['compound'] for x in highTop['text'].apply(sid.polarity_scores)]).mean()
pd.Series([x['compound'] for x in highBot['text'].apply(sid.polarity_scores)]).mean()
pd.Series([x['compound'] for x in lowTop['text'].apply(sid.polarity_scores)]).mean()
pd.Series([x['compound'] for x in lowBot['text'].apply(sid.polarity_scores)]).mean()
