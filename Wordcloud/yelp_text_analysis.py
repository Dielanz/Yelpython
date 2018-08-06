import numpy as np
import pandas as pd
import wordcloud
import matplotlib.pyplot as plt
import statsmodels.api as sm
from nltk.sentiment.vader import SentimentIntensityAnalyzer

rev = pd.read_csv('yelp_reviews_CLEANED.csv')
usr = pd.read_csv('yelp_users_CLEANED.csv')

top = rev[rev['stars'] == 5].sample(n=10000)
bot = rev[rev['stars'] == 1].sample(n=10000)

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

plt.hist(usr[usr['review_count'] == 1]['average_stars'])
plt.hist(usr[usr['review_count'] > 68]['average_stars'])

sid = SentimentIntensityAnalyzer()

high = pd.DataFrame(usr[usr['review_count'] > 68]['user_id'])
low = pd.DataFrame(usr[usr['review_count'] == 1]['user_id'])

highTop = pd.merge(rev[rev['stars'] == 5], high, on='user_id', how='inner').sample(n=10000)
highBot = pd.merge(rev[rev['stars'] == 1], high, on='user_id', how='inner').sample(n=10000)
lowTop = pd.merge(rev[rev['stars'] == 5], low, on='user_id', how='inner').sample(n=10000)
lowBot = pd.merge(rev[rev['stars'] == 1], low, on='user_id', how='inner').sample(n=10000)

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