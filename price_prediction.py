import pandas as pd
import numpy as np
from matplotlib import pyplot as plt
import matplotlib
matplotlib.rcParams["figure.figsize"] = (20,10)

## importing the dataset

data_set = pd.read_csv("Bengaluru_House_Data.csv")
data_set.head()

## creating a new data set by droping some columns from actual data set

new_data_set = data_set.drop(['area_type', 'society', 'balcony', 'availability'],axis = 'columns')
new_data_set.head()

## Data set cleaning process

new_data_set.isnull().sum()

## Drop some data after find out the corrupted data and check again the previous process

new_data_set1 = new_data_set.dropna()
new_data_set1.isnull().sum()
new_data_set1.shape

## creating a new column using the existing column and apply some function to it

new_data_set1['size'].unique()
new_data_set1['Bhk'] = new_data_set1['size'].apply(lambda x: int(x.split(' ')[0]) )
new_data_set1['Bhk'].unique()

## creating a simple function to find out float value in total_sqft column

def is_float(x):
    try:
        float(x)
    except:
        return False
    return True

new_data_set1[~new_data_set1['total_sqft'].apply(is_float)].head(20)

## creating a function to convert the range data to a normal float data

def convert_sqft_to_num(x):
    temp = x.split('-')
    if len(temp) == 2:
        return (float(temp[0])+float(temp[1]))/2
    try:
        return float(x)
    except:
        return None
    
new_data_set2 = new_data_set1.copy()
new_data_set2['total_sqft'] = new_data_set2['total_sqft'].apply(convert_sqft_to_num)
new_data_set2.head(10)  


    
## Creating a new data_Set using the old one & creating a new column using price & sqft 

new_data_set3 = new_data_set2.copy()
new_data_set3['price_per_sqft'] = new_data_set3['price']*100000/new_data_set3['total_sqft']
new_data_set3.head()

## Check the location data

new_data_set3.location.unique()
new_data_set3.location = new_data_set3.location.apply(lambda x: x.strip())
location_finder = new_data_set3.groupby('location')['location'].agg('count').sort_values(ascending=False)
location_finder

len(location_finder[location_finder<=10])

location_finder_less_than_10 = location_finder[location_finder<=10]
location_finder_less_than_10

new_data_set3.location = new_data_set3.location.apply(lambda x: 'other' if x in location_finder_less_than_10 else x)
len(new_data_set3.location.unique())

## Try to find the outlier from data 

data_set_4 = new_data_set3[~(new_data_set3.total_sqft/new_data_set3.Bhk<300)]
data_set_4.shape                           
                           
data_set_4.price_per_sqft.describe() 








