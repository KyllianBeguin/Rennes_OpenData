'''
Name : Rennes traffic

Purpose : Extract data from Open Data Rennes (https://data.rennesmetropole.fr)

Version : 1.0 (10/02/2021)
'''

### Import Section

import time, pandas as pd, requests
from datetime import datetime
# time: used for time.sleep()
# pandas: to manipulate data frames
# requests: to extract data from web and turn it into .json file
# datetime: Used for logs



# Method definition

def Traffic_Crawler(url):

    # Step 1: Extract data and turn it into into a dict from the .json file
    response = requests.get(url).json()
    res = dict((k, response[k]) for k in ['records'] if k in response)



    # Step 2: Create the big dataframe that will contains the extracted data for selected variables
    Col_to_select = ['datetime', 'traveltimereliability', 'denomination', 'trafficstatus', 'averagevehiclespeed', 'traveltime',
              'predefinedlocationreference'] # List of variables
    big_df = pd.DataFrame(columns=Col_to_select) # At first, the big dataframe is just an empty one that need to be filled

    # Turn the dict into a dataframe.
    # Each row will contain a bunch of information that needs to be turned into a dict and into a DataFrame to keep the keys as column.
    # Keys will correspond to Col_to_select, so it will be easier to concat the data frame from each row to the big data frame.
    df = pd.DataFrame(res) # Make the dataframe from the dict. Each row is one individual (a location, predefinedlocationreference)
    for i in range(len(df)):
        df_fields = df.iloc()[i]['records'] # Get the row number i
        dict_fields = dict((k, df_fields[k]) for k in ['fields'] if k in df_fields) # Turn the content into a dict
        df2 = pd.DataFrame(dict_fields) # Turn the dict into a data frame, keys will be columns

        if 'denomination' in list(df2.T.columns): # I just want the location that are labeled, like 'Rue Saint-Hélier' or ' Boulevard de la Liberté'
            big_df = pd.concat([big_df, df2.T[Col_to_select]]) # Concat the big data frame and the data frame (row number i), but only select columns from Col_to_select



    # Step 3: Clean the big data frame
    big_df.reset_index(drop=True, inplace=True) # As we droped some rows, we need to reset the index.
    # [NOT mandatory] In case there is data management or machine learning, it would be interesting to have date related columns
    big_df.datetime = pd.to_datetime(big_df.datetime)
    big_df['year'] = big_df.datetime.dt.year
    big_df['month'] = big_df.datetime.dt.month
    big_df['day'] = big_df.datetime.dt.day
    big_df['hour'] = big_df.datetime.dt.hour
    big_df['minute'] = big_df.datetime.dt.minute
    # Section/Direction columns
    big_df['Section'] = '' # Create column for section, the part of a row
    big_df['Direction'] = '' # Create column for direction, it could be left or right side of the Section
    for i in range(len(big_df)):
        loc_split = big_df.predefinedlocationreference[i].split('_') # Split the predefinedlocationreference value
        # Some values don't contain a Direction as it is a one way or that left and right are not splited
        if len(loc_split) == 2: # If there is a Section AND a Direction
            big_df.loc[i, 'Section'] = loc_split[0]
            big_df.loc[i, 'Direction'] = loc_split[1]
        else:
            big_df.loc[i, 'Section'] = loc_split[0]
            big_df.loc[i, 'Direction'] = 'GD_OneWay' # No specified direction, it could be everything



    # Step 4: Concat old and new information
    df02 = pd.read_csv('Traffic_rennais.csv') # Read existing data frame
    df_final = pd.concat([big_df, df02]) # Concat old and new data frames
    df_final.to_csv('Traffic_rennais.csv', index=False) # Overwrite the existing file




### Main programm

url = 'https://data.rennesmetropole.fr/api/records/1.0/search/?dataset=etat-du-trafic-en-temps-reel&q=&rows=2367&facet=denomination' # First load the url
nb = 1 # Increment

while True:
    Traffic_Crawler(url) # Run the Crawler
    print('Done extracting number ', nb, '\n', '[TIME] ', datetime.now().hour, 'h ', datetime.now().minute, 'mins', sep='') # log
    nb += 1
    time.sleep(3600) # Wait 1 hour (3600 seconds)
    # Reload the url
    url = 'https://data.rennesmetropole.fr/api/records/1.0/search/?dataset=etat-du-trafic-en-temps-reel&q=&rows=2367&facet=denomination'
