import numpy as np
import pandas as pd
import os
import wordcloud
import matplotlib.pyplot as plt

# Filter by city as well

os.chdir("C:\\Users\\LynchZ20\\Desktop\\Summer Classes\\CS\\final_project\\Data")

bus = pd.read_csv('yelp_business.csv')
lst = []
for i in list(bus['categories']):
    lst.extend(i.split(';'))
lst = sorted(list(set(lst)))

bus['restaurant'] = bus['categories'].str.contains('Restaurants')
res = bus[bus['restaurant'] == True]

top = pd.DataFrame(res[res['stars'] == 5]['business_id'])
bot = pd.DataFrame(res[(res['stars'] == 1) | (res['stars'] == 1.5)]['business_id'])
cities = res[res['city'].isin(['Las Vegas', 'Phoenix', 'Toronto', 'Charlotte', 'Scottsdale',
                             'Pittsburgh', 'Mesa', 'Montréal'])]
citiesTop = pd.merge(cities, top, on='business_id', how='inner')
citiesBot = pd.merge(cities, bot, on='business_id', how='inner')
cities = cities[['business_id', 'city']]
citiesTop = citiesTop[['business_id', 'city']]
citiesBot = citiesBot[['business_id', 'city']]

del(bus, lst, i, res)

rev = pd.read_csv('yelp_review.csv')

topR = pd.merge(rev, top, on='business_id', how='inner')
botR = pd.merge(rev, bot, on='business_id', how='inner')
citR = pd.merge(rev, cities, on='business_id', how='inner')
citTR = pd.merge(rev, citiesTop, on='business_id', how='inner')
citBR = pd.merge(rev, citiesBot, on='business_id', how='inner')


del(rev, top, bot, cities, citiesTop, citiesBot)

def collectStrings(series):
    fullText = ''
    for txt in list(series):
        fullText += txt
    return fullText

txt = {}
txt.update({'top': collectStrings(topR['text'])})
txt.update({'bottom': collectStrings(botR['text'])})
city = 'Las Vegas'
for city in ['Las Vegas', 'Phoenix', 'Toronto', 'Charlotte', 'Scottsdale',
                             'Pittsburgh', 'Mesa', 'Montréal']:
    txt.update({city: collectStrings(citR[citR['city'] == city].sample(n=20000)['text'])})
    txt.update({city + '_Top': collectStrings(citTR.loc[citTR['city'] == city, 'text'])})
    txt.update({city + '_Bot': collectStrings(citBR.loc[citBR['city'] == city, 'text'])})
    print(city)

for key, val in txt.items():
    print(str(key) + ': ')
    wc = wordcloud.WordCloud(max_font_size=40).generate(val)
    plt.figure(figsize=(12,9), facecolor='w')
    plt.imshow(wc, interpolation="bilinear")
    plt.imshow(wc)
    plt.axis("off")
    plt.savefig(str(key) + '.png')
    plt.show()

topTxt = collectStrings(topR['text'])
botTxt = collectStrings(botR['text'])
lvTxt = collectStrings(citR[citR['city'] == 'Las Vegas'].sample(n=20000)['text'])
phTxt = collectStrings(citR[citR['city'] == 'Phoenix'].sample(n=20000)['text'])
trTxt = collectStrings(citR[citR['city'] == 'Toronto'].sample(n=20000)['text'])
chTxt = collectStrings(citR[citR['city'] == 'Charlotte'].sample(n=20000)['text'])
scTxt = collectStrings(citR[citR['city'] == 'Scottsdale'].sample(n=20000)['text'])
ptTxt = collectStrings(citR[citR['city'] == 'Pittsburgh'].sample(n=20000)['text'])
msTxt = collectStrings(citR[citR['city'] == 'Mesa'].sample(n=20000)['text'])
mtTxt = collectStrings(citR[citR['city'] == 'Montréal'].sample(n=20000)['text'])

dd = {'Top': topTxt, 
      'Bottom': botTxt, 
      'Las Vegas': lvTxt, 
      'Phoenix': phTxt, 
      'Toronto': trTxt, 
      'Charlotte': chTxt, 
      'Scottsdale': scTxt, 
      'Pittsburgh': ptTxt, 
      'Mesa': msTxt, 
      'Montréal': mtTxt}
del(topR, botR, citR, topTxt, botTxt, lvTxt, phTxt, trTxt, chTxt, scTxt, ptTxt, msTxt, mtTxt)

os.chdir("C:\\Users\\LynchZ20\\Desktop\\Summer Classes\\CS\\final_project\\Images")

for key, val in dd.items()[0]:
    print(str(key) + ': ')
    wc = wordcloud.WordCloud(max_font_size=40).generate(val)
    plt.figure(figsize=(12,9), facecolor='w')
    #plt.imshow(wc, interpolation="bilinear")
    plt.imshow(wc)
    plt.axis("off")
    plt.savefig(str(key) + '.png')
    plt.show()


