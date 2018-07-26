
import pandas as pd

filenames = ["yelp_"+ x for x in ["business_attributes.csv","business_hours.csv","business.csv","checkin.csv","review.csv","tip.csv","user.csv"]] 

nrows = 100000

df_list = [pd.read_csv(filenames[x],nrows=nrows) for x in range(len(filenames))]

columns_list = [sorted(df_list[x].columns.tolist()) for x in range(len(filenames))]

column_set = set()

for x in range(len(filenames)):
    for y in columns_list[x]:
        column_set.add(y)    
        
data_dict_df = pd.DataFrame(columns=column_set, index = filenames )    

for i , filename in enumerate(filenames):
    print(filename)
    for tple in data_dict_df.loc[filename].iteritems():
        if(tple[0] in columns_list[i]):
            print(tple[0])
            data_dict_df.loc[filename][tple[0]] = 1
        #else: data_dict_df.loc[filename][tple[0]] = 0
            
data_dict_df.to_csv('data_dictionary.csv')            


