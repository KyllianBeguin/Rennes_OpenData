'''
Name : Rennes traffic Analysis

Purpose : Visualize insights for a street

Version : 1.0 (11/02/2021)
'''

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np



def Street_checker(street, df):
    # To check the street inside the big data frame

    # Lowercase denomination and street input
    df.denomination = df.denomination.str.lower()
    street = street.lower()

    # Checker
    if street in df.denomination.unique():
        return street
    else:
        print('Please, enter a valid street name\n')
        street_list = input('Would you like to check the street list ? (y/n) ') # Just in case you are lost
        if street_list == 'y':
            for i in df.denomination.unique():
                print(i)
            print('\n')
        else:
            ask_for_search = input('Would you like to search for a street ? (y/n) ')
            if ask_for_search == 'y':
                street_keyword = input('please, enter one keyword ')
                print('\n')
                for i in df.denomination.unique():
                    j = i.split()
                    if street_keyword in j:
                        print(i)
                    else:
                        pass
                print('\n')
        street = input('Please, enter a street: ') # Try again
        Street_checker(street, df) # And check again !
        return street

def Number_checker(day):
    try:
        day_selected = int(day)
    except ValueError:
        print('\nYou did not enter a valid integer')
        day = input('Please enter a day: ')
        Number_checker(day)
    return int(day)

def initiate_programm():
    df = pd.read_csv('Traffic_rennais.csv')
    street = input('Please, enter a street: ')
    street_checked = Street_checker(street, df)
    day_choosed = input('Please enter a day: ')
    day_checked = Number_checker(day_choosed)
    return df, street_checked, day_checked

def StreetDayAverage(street, df, day):

    # Step 02: turn day_choosed as a integer (have been chacked before)
    day_choosed = int(day)

    # Step 01: Filter the data frame
    df_choosedDayStreet = df[(df.day == day_choosed) & (df.denomination == street)]
    ListHours_for_plot = df_choosedDayStreet.hour.unique()

    # Step 02: Make the average for each hour for specified street and hour
    ListMean_for_plot = []
    for i in df_choosedDayStreet.hour.unique():
        ListMean_for_plot.append(round(df_choosedDayStreet[df_choosedDayStreet.hour == i].averagevehiclespeed.mean(), 2))

    # Step 03: Plot it
    fig, ax = plt.subplots(figsize=(15, 6))
    x = np.arange(len(ListHours_for_plot))
    rect = ax.plot(x, ListMean_for_plot[::-1])
    ax.set_xticks(x)
    ax.set_xticklabels(ListHours_for_plot[::-1])
    title = 'Vitesse Moyenne\n['+str(street)+']'

    plt.title(title)
    plt.show()





df, street_checked, day_checked = initiate_programm()

StreetDayAverage(street_checked, df, day_checked)