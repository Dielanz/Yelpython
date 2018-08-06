# The purpose of this file is to scrape the city-data website,
# get the population and per capita income from there, and
# output new file with an additional column with tuples
# (population, income)

from numpy import *
from pandas import *

import urllib.request, urllib.parse, urllib.error
from bs4 import BeautifulSoup
import re


infile = 'yelp_business.csv'
outfile = 'yelp_business_pop_income_append.csv'

states_dict = {
        'AK': 'Alaska',
        'AL': 'Alabama',
        'AR': 'Arkansas',
        'AS': 'American Samoa',
        'AZ': 'Arizona',
        'CA': 'California',
        'CO': 'Colorado',
        'CT': 'Connecticut',
        'DC': 'District of Columbia',
        'DE': 'Delaware',
        'FL': 'Florida',
        'GA': 'Georgia',
        'GU': 'Guam',
        'HI': 'Hawaii',
        'IA': 'Iowa',
        'ID': 'Idaho',
        'IL': 'Illinois',
        'IN': 'Indiana',
        'KS': 'Kansas',
        'KY': 'Kentucky',
        'LA': 'Louisiana',
        'MA': 'Massachusetts',
        'MD': 'Maryland',
        'ME': 'Maine',
        'MI': 'Michigan',
        'MN': 'Minnesota',
        'MO': 'Missouri',
        'MP': 'Northern Mariana Islands',
        'MS': 'Mississippi',
        'MT': 'Montana',
        'NA': 'National',
        'NC': 'North Carolina',
        'ND': 'North Dakota',
        'NE': 'Nebraska',
        'NH': 'New Hampshire',
        'NJ': 'New Jersey',
        'NM': 'New Mexico',
        'NV': 'Nevada',
        'NY': 'New York',
        'OH': 'Ohio',
        'OK': 'Oklahoma',
        'OR': 'Oregon',
        'PA': 'Pennsylvania',
        'PR': 'Puerto Rico',
        'RI': 'Rhode Island',
        'SC': 'South Carolina',
        'SD': 'South Dakota',
        'TN': 'Tennessee',
        'TX': 'Texas',
        'UT': 'Utah',
        'VA': 'Virginia',
        'VI': 'Virgin Islands',
        'VT': 'Vermont',
        'WA': 'Washington',
        'WI': 'Wisconsin',
        'WV': 'West Virginia',
        'WY': 'Wyoming'
}

## read in file
data = read_csv(infile)

## convert 'chapel hill' 'NC' to 'chapel-hill-north-carolina'
data['city_state'] = data['city'] +' ' + data['state'].map(states_dict)

#Replace spaces with hyphens to be able to match the format needed to webscrape
data['city_state'] = data['city_state'].str.replace(' ','-')

#Create an empty dictionary
pop_income_dict = {}

count = 0

#For every unique city and state, get population and income
for i in data['city_state']:

    # check if we already looked up the city
    if i in pop_income_dict.keys():
        continue

    else:
        ## ignore international cities
        if isnull(i):
            continue
        else:
            try:
                ## load url and parse page
                city_data_url = 'http://www.city-data.com/city/'+ i + '.html'
                print(city_data_url)

                webpage_city = urllib.request.urlopen(city_data_url)
                data_city = webpage_city.read().decode()
                soup_city = BeautifulSoup(data_city, 'html.parser')

            # ignore small towns/districts with no census data
            except:
                pop_income_dict[i] = NaN

            # find population
            population = soup_city.find_all('section', class_='city-population')[0].text

            # Extract population data using regular expressions
            population = re.findall('Population in .+:\s(\d{1,3}[,\d]+)',population)[0]

            #Remove comma from population data and typecast to integer
            population = int(population.replace(',','').replace('.',''))

            # find median household income
            income_data = soup_city.find_all('section', class_='median-income')[0].text

            # Extract income data using regular expressions
            per_cap_income = re.findall('Estimated per capita income in 2016: \$([,\d]{1,7})',income_data)

            #Remove comma and period from income data and typecast to integer
            per_cap_income = int(per_cap_income[0].replace(',','').replace('.',''))

            ## update dictionary
            ## print(i, population, per_cap_income)
            pop_income_dict[str(i)] = (population,per_cap_income)

#Maps a new column from of tuples (population,income) for each city
data['pop_income'] = data['city_state'].map(pop_income_dict)

#Write new file with population and income data appended. This file becomes the input to Clean_Yelp_Files.py
data.to_csv(outfile)
