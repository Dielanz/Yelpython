# creates a csv file for our clean_yelp_files.py program
# it outputs a csv file with a "False" in front of each column. We then can
# turn any columns to a "True" and our main datacleaning file will use them. 


import pandas as pd

#Create a list of filenames
filenames = ["yelp_"+ x for x in ["business_hours.csv","business.csv","review.csv","user.csv"]]

#Number of rows to read in
nrows = 1000

#Create a list of DataFrames (the first 100K rows of each csv)
df_list = [pd.read_csv(filenames[x],nrows=nrows) for x in range(len(filenames))]

#Create a list of columns for the output file
columns_list = [df_list[x].columns.tolist() for x in range(len(filenames))]

data_dict_df = pd.DataFrame(columns=["file","columnName", "keep"])

for index in range(len(columns_list)):
    for column in range(len(columns_list[index])):
        if str(columns_list[index][column]) in ("business_id", "user_id"):
            continue # Skip the ID columns
        data_dict_df = data_dict_df.append(pd.Series([str(filenames[index]).replace(".csv",""), columns_list[index][column], True], index=['file', 'columnName','keep']), ignore_index=True)

#Write df to csv
data_dict_df.to_csv('columnNames.csv')
