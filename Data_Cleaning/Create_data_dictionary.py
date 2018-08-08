# Group: yelPython
# Members: Ruslan Askerov (ra7kv), Will Daniel (wkd9th), Zach Lynch (zsl2gf), Le Michael Song (ls2ywj), Dylan Weber (dew2ad)


# A program for creating the data dictionary for the entire data that we use.

import pandas as pd

#Create a list of filenames
filenames = ["yelp_"+ x for x in ["business_attributes.csv","business_hours.csv","business.csv","checkin.csv","review.csv","tip.csv","user.csv"]]

#Number of rows to read in
nrows = 100000

#Create a list of DataFrames (the first 100K rows of each csv)
df_list = [pd.read_csv(filenames[x],nrows=nrows) for x in range(len(filenames))]

#Create a list of columns of each data frame
columns_list = [df_list[x].columns.tolist() for x in range(len(filenames))]

column_set = set()

#Add each column name to the set
for x in range(len(filenames)):
    for y in columns_list[x]:
        column_set.add(y)

#Sort the set
column_set = sorted(column_set, key=lambda x : x[0].upper())

#Create an empty df
data_dict_df = pd.DataFrame(columns=column_set, index = filenames )

#Add data to the df (which tables have which columns?)
for i , filename in enumerate(filenames):
    #print(filename)
    for tple in data_dict_df.loc[filename].iteritems():
        if(tple[0] in columns_list[i]):
            #print(tple[0])
            data_dict_df.loc[filename][tple[0]] = 1
        #else: data_dict_df.loc[filename][tple[0]] = 0

#Write df to csv
data_dict_df.to_csv('data_dictionary.csv')
