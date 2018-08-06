import numpy as np
import pandas as pd
import wordcloud
import matplotlib.pyplot as plt
import statsmodels.api as sm
from nltk.sentiment.vader import SentimentIntensityAnalyzer

res = pd.read_csv('yelp_restaurants_CLEANED.csv')
rev = pd.read_csv('yelp_reviews_CLEANED.csv')
usr = pd.read_csv('yelp_users_CLEANED.csv')

top = pd.DataFrame(res[res['stars'] == 5]['business_id'])
bot = pd.DataFrame(res[(res['stars'] == 1) | (res['stars'] == 1.5)]['business_id'])

def collectStrings(series):
    fullText = ''
    for txt in list(series):
        fullText += txt
    return fullText

topR = pd.merge(rev, top, on='business_id', how='inner')
botR = pd.merge(rev, bot, on='business_id', how='inner')

txt = {}
txt.update({'top': collectStrings(topR['text'])})
txt.update({'bot': collectStrings(botR['text'])})
for key, val in txt.items():
    print(str(key) + ': ')
    wc = wordcloud.WordCloud(max_font_size=40).generate(val)
    plt.figure(figsize=(12,9), facecolor='w')
    plt.imshow(wc, interpolation="bilinear")
    plt.imshow(wc)
    plt.axis("off")
    plt.savefig(str(key) + '.png')
    plt.show()

plt.hist(usr[usr['review_count'] == 1]['average_stars'])
plt.hist(usr[usr['review_count'] > 68]['average_stars'])

sid = SentimentIntensityAnalyzer()

high = pd.DataFrame(usr[usr['review_count'] > 68]['user_id'])
low = pd.DataFrame(usr[usr['review_count'] == 1]['user_id'])

highTop = pd.merge(pd.merge(rev, top, on='business_id', how='inner'), high, on='user_id', how='inner')
highBot = pd.merge(pd.merge(rev, bot, on='business_id', how='inner'), high, on='user_id', how='inner')
lowTop = pd.merge(pd.merge(rev, top, on='business_id', how='inner'), low, on='user_id', how='inner')
lowBot = pd.merge(pd.merge(rev, bot, on='business_id', how='inner'), low, on='user_id', how='inner')

pd.Series([x['compound'] for x in highTop['text'].apply(sid.polarity_scores)]).mean()
pd.Series([x['compound'] for x in highBot['text'].apply(sid.polarity_scores)]).mean()
pd.Series([x['compound'] for x in lowTop['text'].apply(sid.polarity_scores)]).mean()
pd.Series([x['compound'] for x in lowBot['text'].apply(sid.polarity_scores)]).mean()

revTest = rev.sample(n=50000).reset_index(drop=True)
revTest['sentiment'] = [x['compound'] for x in revTest['text'].apply(sid.polarity_scores)]

indep = revTest['sentiment']
targ = revTest['stars']
model = sm.OLS(targ, indep).fit()
model.summary()