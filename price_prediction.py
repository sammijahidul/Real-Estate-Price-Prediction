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

def remove_outliers(df):
    df_out = pd.DataFrame()
    for key, subdf in df.groupby('location'):
        m = np.mean(subdf.price_per_sqft)
        st = np.std(subdf.price_per_sqft)
        reduced_df = subdf[(subdf.price_per_sqft>(m-st)) & (subdf.price_per_sqft<(m+st))]
        df_out = pd.concat([df_out,reduced_df], ignore_index=True)
    return df_out    



data_set_5 = remove_outliers(data_set_4)
data_set_5.shape 

def plot_scatter_chart(df,location):
    bhk2 = df[(df.location==location) & (df.Bhk==2)]
    bhk3 = df[(df.location==location) & (df.Bhk==3)]
    matplotlib.rcParams['figure.figsize'] = (15,10)
    plt.scatter(bhk2.total_sqft, bhk2.price, color='blue', label='2 BHK', s=50)
    plt.scatter(bhk3.total_sqft, bhk3.price,marker ='+', color='green', label='3 BHK', s=50)
    plt.xlabel("Total Suare Feet Area")
    plt.ylabel("Price")
    plt.title(location)
    plt.legend()
    
plot_scatter_chart(data_set_5, "Rajiji Nagar")    
    
 
def remove_bhk_outliers(df):
    exclude_indices = np.array([])
    for location, location_df in df.groupby('location'):
        bhk_stats = {}
        for bhk, bhk_df in location_df.groupby('Bhk'):
            bhk_stats[bhk] = {
                'mean': np.mean(bhk_df.price_per_sqft),
                'std': np.std(bhk_df.price_per_sqft),
                'count': bhk_df.shape[0]
            }
        for bhk, bhk_df in location_df.groupby('Bhk'):
            stats = bhk_stats.get(bhk-1)
            if stats and stats['count']>5:
                exclude_indices = np.append(exclude_indices, 
                                            bhk_df[bhk_df.price_per_sqft<(stats['mean'])].index.values)
    return df.drop(exclude_indices, axis='index')    

data_set_6 = remove_bhk_outliers(data_set_5) 
data_set_6.shape      

import matplotlib
matplotlib.rcParams['figure.figsize'] = (20,10)
plt.hist(data_set_6.price_per_sqft,rwidth=0.8)
plt.xlabel('Price per square feet')
plt.ylabel('count')

#data_set_6[data_set_6.bath>10]

plt.hist(data_set_6.bath,rwidth=0.8)
plt.xlabel("Number of bathrooms")
plt.ylabel("Count")

data_set_6[data_set_6.bath>data_set_6.Bhk+2]

data_set_7 = data_set_6[data_set_6.bath<data_set_6.Bhk+2]
data_set_7.shape



