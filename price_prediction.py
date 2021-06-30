import pandas as pd
import numpy as np
from matplotlib import pyplot as plt
import matplotlib
matplotlib.rcParams["figure.figsize"] = (20,10)

data_set = pd.read_csv("Bengaluru_House_Data.csv")
data_set.head()

# creating a new data set by droping some columns from actual data set

new_data_set = data_set.drop(['area_type', 'society', 'balcony', 'availability'],axis = 'columns')
new_data_set.head()

# Data set cleaning process

new_data_set.isnull().sum()

# Drop some data after find out the corrupted data and check again the previous process

new_data_set1 = new_data_set.dropna()
new_data_set1.isnull().sum()
new_data_set1.shape

# creating a new column using the existing column and apply some function to it

new_data_set1['size'].unique()
new_data_set1['Bhk'] = new_data_set1['size'].apply(lambda x: int(x.split(' ')[0]) )

#






