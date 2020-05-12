# %%
# data analysis and wrangling
import pandas as pd
import numpy as np
import random as rnd
# visualization
import seaborn as sns
import matplotlib.pyplot as plt
#%matplotlib inline
# machine learning
from sklearn import neighbors
from sklearn.neighbors import KNeighborsRegressor
from sklearn import preprocessing

# %%
data = pd.read_csv('csv/data.csv') 
# %%
train_df = pd.read_csv('csv/train.csv') 
test_df = pd.read_csv('csv/test.csv') 

# %%
X_train = train_df.drop('MAGNITUDE', axis=1)
Y_train = train_df['MAGNITUDE']
X_test  = test_df.drop('MAGNITUDE', axis = 1)
Y_test = test_df['MAGNITUDE']

# %%
df1 = data[['HOURS', 'MAGNITUDE']].groupby(['HOURS'], as_index=False).count().sort_values(by='MAGNITUDE', ascending=False)

# %%
df2 = data[data['YEAR'] >= 2010]
df2 = df2[['YEAR', 'MAGNITUDE']].groupby(['YEAR'], as_index=False).count().sort_values(by='YEAR', ascending=False)

# %%
df3 = {'data_description': ['mean','min','25%','50%', '75%', 'max'],
         'MAGNITUDE': [3.15, 2.6 , 2.8, 3.1, 3.4, 8]
        }
df3 = pd.DataFrame(df3,columns=['data_description','MAGNITUDE'])

# %%
x_train_scaled = preprocessing.scale(X_train)
X_train = pd.DataFrame(x_train_scaled)

x_test_scaled = preprocessing.scale(X_test)
X_test = pd.DataFrame(x_test_scaled)

# %%
model = neighbors.KNeighborsRegressor(n_neighbors = 3)

model.fit(X_train, Y_train)  #fit the model
pred=model.predict(X_test) #make prediction on test set
acc_model = round(model.score(X_train, Y_train) * 100, 2)
X_test['MAGNITUDE'] = pred

X_test.to_csv('C:\\Users\\HP\\Desktop\\PEG\\csv\\result.csv', index = False)