import pandas as pd 
import matplotlib.pyplot as plt
import math
import numpy as np
import seaborn as sns

yelp_scatter = pd.read_csv('yelp_rest_hours.csv', index_col = 'business_id')

#yelp_scatter = yelp_scatter.loc[:, ['stars', 'pop_income']]

yelp_scatter[['population','income']] = yelp_scatter['pop_income'].str.split(',',expand=True)

yelp_scatter['income'] = yelp_scatter['income'].map(lambda x: str(x)[:-1])
yelp_scatter['population'] = yelp_scatter['population'].map(lambda x: str(x)[1:])

yelp_scatter['population'] = pd.to_numeric(yelp_scatter['population'], errors='coerce')
yelp_scatter['income'] = pd.to_numeric(yelp_scatter['income'], errors='coerce')

yelp_scatter['log_income'] = yelp_scatter['income'].apply(math.log)
yelp_scatter['log_pop'] = yelp_scatter['population'].apply(math.log)

yelp_scatter = yelp_scatter[yelp_scatter['review_count'] > 20]



# CREATE A SCATTERPLOT
yelp_scatter.plot.scatter(x = 'log_pop', y = 'stars')
yelp_scatter.plot.scatter(x = 'log_income', y = 'stars')

states = list(set(yelp_scatter['state']))
stars = list(set(yelp_scatter['stars']))



for state in states:
    plt.figure()
    yelp_state = yelp_scatter[yelp_scatter['state']==state]
    plot = sns.countplot(x = yelp_state['stars'], data=yelp_state, color = 'r', alpha = 0.7)
    plt.title(state)
    mean = np.mean(yelp_state['stars'])
    print("The average star rating for "+str(state) +" is " + str(mean))
    
