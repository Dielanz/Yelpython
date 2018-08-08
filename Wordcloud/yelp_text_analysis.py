# Group: yelPython
# Members: Ruslan Askerov (ra7kv), Will Daniel (wkd9th), Zach Lynch (zsl2gf), Le Michael Song (ls2ywj), Dylan Weber (dew2ad)


# Text analysis program. Creates a wordcloud. And conducts a sentiment analysis.

import numpy as np
import pandas as pd
import wordcloud
import matplotlib.pyplot as plt
import statsmodels.api as sm
from nltk.sentiment.vader import SentimentIntensityAnalyzer

#Read in yelp review and user data
rev = pd.read_csv('yelp_reviews_CLEANED.csv')
usr = pd.read_csv('yelp_users_CLEANED.csv')

#Get a sample of 5-star and 1-star reviews for word cloud comparison
top = rev[rev['stars'] == 5].sample(n=10000)
bot = rev[rev['stars'] == 1].sample(n=10000)

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
    wc = wordcloud.WordCloud(max_font_size=40, background_color='white').generate(val)
    plt.figure(figsize=(8,6), facecolor='w')
    plt.imshow(wc)
    plt.axis("off")
    plt.savefig(str(key) + '.png')
    plt.show()

#Create histogram of users with one review ONLY by number of stars
plt.hist(usr[usr['review_count'] == 1]['average_stars'], bins=10)
plt.xlabel('Avg Rating')
plt.ylabel('User Count')

#Create histogram of users with at least 69 reviews by number of stars
# We use 69 because 10% of users have 1 review and 10% of reviews have more than 68 
plt.hist(usr[usr['review_count'] > 68]['average_stars'], bins=10)
plt.xlabel('Avg Rating')
plt.ylabel('User Count')

#Initializes sentiment analyzer
sid = SentimentIntensityAnalyzer()

#Create dataframes of users similar to the data used in the histograms above (1 review and more than 68)
high = pd.DataFrame(usr[usr['review_count'] > 68]['user_id'])
low = pd.DataFrame(usr[usr['review_count'] == 1]['user_id'])

#Split the two groups into four by adding the 5 star or 1 star dimension (sample 10000 for each group)
highTop = pd.merge(rev[rev['stars'] == 5], high, on='user_id', how='inner').sample(n=10000)
highBot = pd.merge(rev[rev['stars'] == 1], high, on='user_id', how='inner').sample(n=10000)
lowTop = pd.merge(rev[rev['stars'] == 5], low, on='user_id', how='inner').sample(n=10000)
lowBot = pd.merge(rev[rev['stars'] == 1], low, on='user_id', how='inner').sample(n=10000)

#Get the mean compound polarity score for each group above (highTop, highBot, lowTop, lowBot)
pd.Series([x['compound'] for x in highTop['text'].apply(sid.polarity_scores)]).mean()
pd.Series([x['compound'] for x in highBot['text'].apply(sid.polarity_scores)]).mean()
pd.Series([x['compound'] for x in lowTop['text'].apply(sid.polarity_scores)]).mean()
pd.Series([x['compound'] for x in lowBot['text'].apply(sid.polarity_scores)]).mean()

#Creating a quick model to understand the relationship between review count and sentiment
revTest = rev.sample(n=50000).reset_index(drop=True)
revTest['sentiment'] = [x['compound'] for x in revTest['text'].apply(sid.polarity_scores)]

#Set dep, indep variables for the model and fit it
indep = revTest['sentiment']
targ = revTest['stars']
model = sm.OLS(targ, indep).fit()
model.summary()
