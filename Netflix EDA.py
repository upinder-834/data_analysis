#!/usr/bin/env python
# coding: utf-8

# In[1]:


import numpy as np
import pandas as pd
import os
import re

import matplotlib.pyplot as plt
import seaborn as sns

get_ipython().run_line_magic('matplotlib', 'inline')

pd.options.display.float_format = '{:,.2f}'.format


# In[2]:


netflix = pd.read_csv('./training/netflix_titles.csv')

print(f'DataFrame Details\n')
print(f'Total Rows: {netflix.shape[0]}\nTotal Columns: {netflix.shape[1]}')
display(netflix.head())


# #### Data processing

# In[3]:


# remove NaN
netflix = netflix.drop(netflix[netflix.isnull().any(axis=1)].index)

# add column for year added and age
netflix['year_added'] = netflix['date_added'].apply(lambda x: str(x)[-4:])
netflix['year_added'] = netflix['year_added'].astype('int64')
netflix['show_age'] = 2021 - netflix['year_added']
netflix['show_age'] = netflix['show_age'].apply(lambda x: str(x)+' year(s)')

# drop extra columns
netflix.drop(['show_id','date_added','release_year','description'],axis=1,inplace=True)

print('Data processing done')
display(netflix.head())


# #### Data Analysis

# In[4]:


fig, ax = plt.subplots(1,2,figsize=(12,6))
fig.tight_layout(pad=5)

sns.countplot(data=netflix,x='type',ax=ax[0])
ax[0].set_title('Content Type')
sns.boxplot(x='type',y='year_added',data=netflix,ax=ax[1])
ax[1].set_title('Content Production')
plt.show()


# In[5]:


age = netflix['show_age'].value_counts()[:10]
age.plot(kind='bar',title='Content Age',figsize=(13,8))


# In[6]:


plt.figure(figsize=(12,6))
types = list(netflix.type.unique())

for i in range(len(types)):
    plt.subplot(1,2,i+1)
    if types[i] == 'Movie':
        movies = netflix[netflix.type == types[i]]
        movies = movies.duration.value_counts()[:10]
        movies.plot(kind='bar')
    elif types[i] == 'TV Show':
        tv_show = netflix[netflix.type == types[i]]
        tv_show = tv_show.duration.value_counts()[:10]
        tv_show.plot(kind='bar')
    plt.title(f'Top 10 {types[i]} Duration')
    plt.xticks(rotation=45)
    
plt.tight_layout(pad=5)


# In[7]:


plt.figure(figsize=(12,6))

for i in range(len(types)):
    plt.subplot(1,2,i+1)
    if types[i] == 'Movie':
        movies = netflix[netflix.type == 'Movie']
        movies = movies.country.value_counts()[:10]
        movies.plot(kind='bar',title=f'Top 10 Countries for {types[i]} Production')
    elif types[i] == 'TV Show':
        tv_show = netflix[netflix.type == 'TV Show']
        tv_show = tv_show.country.value_counts()[:10]
        tv_show.plot(kind='bar',title=f'Top 10 Countries for {types[i]} Production')

plt.tight_layout(pad=5)


# In[8]:


plt.figure(figsize=(15,5))

countries = netflix.country.value_counts()[:10].index
for i in range(len(countries)):
    plt.subplot(2,5,i+1)
    x = netflix[netflix.country == countries[i]]
    x = x.type.value_counts()
    x.plot(kind='bar')
    plt.title(f'Movie vs. TV Show in {countries[i]}')
    plt.xticks(rotation=360)
    
plt.tight_layout(pad=.8)


# In[9]:


nflx = netflix.copy()
nflx['listed_in'] = nflx['listed_in'].apply(lambda x: x.split(',')[0])

genre = nflx.listed_in.value_counts()[:10]
genre.sort_values().plot(kind='barh',title='Top 10 Most Popular Genre')
plt.show()

