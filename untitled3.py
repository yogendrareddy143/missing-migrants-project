#!/usr/bin/env python
# coding: utf-8

# In[1]:


# This Python 3 environment comes with many helpful analytics libraries installed
# It is defined by the kaggle/python docker image: https://github.com/kaggle/docker-python
# For example, here's several helpful packages to load in 

import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)

# Input data files are available in the "../input/" directory.
# For example, running this (by clicking run or pressing Shift+Enter) will list the files in the input directory

'''import os
print(os.listdir("data set"))'''

# Any results you write to the current directory are saved as output.


# # My first public Kernel in Kaggle
# 
# I have been seriously learning python for DS since April this year.
# 
# I had a vague idea about the language but now I would say I feel more comfortable.
# To understand the language I took a good Udemy course and then decided to do the entire Dataquest path in Python
# 
# What I notice is that the best way to practice is to just get started.
# It will take a while to things look "perfect" and I know I will make lots of mistake and not do things so elegantly at start, but I put a purpose to just get started and like just do things as I go along and google, stack overflow my way to fluency.
# Just at randomly going through a data set and wrangling and analysing you improve your analytical skill.
# In the kernel below I try to do just that and I learn a few things along the way.
# I will keep on adding to it to get to a stage where we can conclude something about this data.
# 

# In[2]:


mg = pd.read_csv('C:/Users/yogi reddy/Desktop/pythonproject/dataset.csv')


# In[3]:


import seaborn as sns
import matplotlib.pyplot as plt
get_ipython().run_line_magic('matplotlib', 'inline')
from datetime import datetime


# In[4]:


mg.head(3)


# In[5]:


mg.shape


# In[6]:


mg.info()


# In[7]:


mg['Region of Incident'].value_counts().plot.bar()


# In[8]:


pd.pivot_table(mg,values='Total Dead and Missing',index='Reported Date',aggfunc=np.sum).sort_index().head()
# Cannot sort as the date is a string and do not like to see in alphabetical order
# Will Create a date field


# In[9]:


# Found a good article here https://www.datacamp.com/community/tutorials/converting-strings-datetime-objects


# In[10]:


#Get one scalar to learn the new function
date_s = mg.iloc[1,2]
date_s


# In[11]:


date_test = datetime.strptime(date_s,'%B %d, %Y')
print(date_test)


# In[12]:


#now create a new proper datetime column
mg['Reported Date dt']= mg['Reported Date'].apply(lambda x: datetime.strptime(x,'%B %d, %Y'))


# In[13]:


pd.pivot_table(mg,values='Total Dead and Missing',index='Reported Date dt',aggfunc=np.sum).sort_index().plot()


# In[14]:


pd.pivot_table(mg,values='Total Dead and Missing',index='Reported Year',aggfunc=np.sum).sort_index().plot(kind='bar')


# In[15]:


# Visualise a table per year with number of dead
pd.pivot_table(mg,values='Total Dead and Missing',index='Reported Year',aggfunc=np.sum).sort_index()


# In[16]:


print('Maximum date is : {}'.format(mg['Reported Date dt'].max()))
# last reported date was end of 1st Quarted 2019
print('Minimum date is : {}'.format(mg['Reported Date dt'].min()))


# Interesting that there was a great report increase in 2015 and 2016 then it came down in the years of 2017 and 2018 with the lowest. Lets not consider 2019 as the year is not yet finish. The latest data is from March 2019. Also need to disregard 2014 for comparison as there is not a full year there.
# As a Data Scientist our first job is to be sceptical until we have clear and objective evidence. 
# We don't really know if all the incidents were reported and if the numbers reported are accurate. 
# One thing that I would think is. Why the numbers went down?
# 
# * International Media pressure?
# * Decrease of conflict, which decreased migration?
# * More humane treatment of migrants by the police coast?
# 

# Let's now visualise the proportion of missing people of Male, Female and Children

# In[17]:



pd.pivot_table(mg,values=['Number of Males','Number of Females','Number of Children'],
               index='Reported Year',
               aggfunc={'Number of Males': np.sum,'Number of Females': np.sum,'Number of Children': np.sum}).plot(kind='bar')


# It looks that the split of male and female and children is not always reported because the total Male and Female is not equals the total number of missing or dead.
# So we cannot simply analyse the data for all, however lets take the proportion of Male Female for those that the total Male+Female=Total Missing or Dead.

# In[18]:


# Create a column that sum Total Male and Female
mg['Total MFC']= mg['Number of Males']+mg['Number of Females']+mg['Number of Children']


# In[19]:


# filter the data frame that meet the criteria and check how many records has with correctly reporting Male and Female
mg[mg['Total MFC']==mg['Total Dead and Missing']].shape[0]


# only 39 reports looks have done "correctly"... not a good thing but let's see anyway

# In[20]:


# Create a dataframe with only the observations with correct report of Male,Female and Children
mg_reportMFC = mg[mg['Total MFC']==mg['Total Dead and Missing']]


# Let's visualise both charts and observe with all data including the non reported MFC and the reported and check if the proportion are similar

# In[21]:


datasets=[mg,mg_reportMFC]

for data in datasets:
    pd.pivot_table(data,values=['Number of Males','Number of Females','Number of Children'],
                   index='Reported Year',
                   aggfunc={'Number of Males': np.sum,'Number of Females': np.sum,'Number of Children': np.sum}).plot(kind='bar')
  


# In[22]:


pd.pivot_table(mg,values=['Number of Males','Number of Females','Number of Children'],
               index='Reported Year',
               aggfunc={'Number of Males': np.sum,'Number of Females': np.sum,'Number of Children': np.sum})



# In[23]:


# transform into tidy format using melt

tidy =pd.pivot_table(mg_reportMFC,values=['Number of Males','Number of Females','Number of Children'],
               index='Reported Year',
               aggfunc={'Number of Males': np.sum,'Number of Females': np.sum,'Number of Children': np.sum})

tidy['year']=tidy.index
pd.melt(tidy,id_vars=['year'])


# It is very similar visually the proportion for both dataframe. In 2016 there are more children than women on the "Correct" data and in 2014 looks like there much more children

# Another oportunity to improve the data is to split location coordinates
# The location coordinates is in only one column and it would be good to split them into to by manipulating string ising the expand property
# 

# In[24]:


# split on ',' coma and expand then rename columns
lat_lon = mg['Location Coordinates'].str.split(',',expand=True).rename(index=int, columns={0: "lat", 1: "lon"})


# In[25]:


#Concat expanded columns
mg =pd.concat([mg,lat_lon],axis=1)


# In[26]:


mg.head()


# In[27]:


# Will attemp use folim to project this in a map
# here is a good page https://alysivji.github.io/getting-started-with-folium.html
# Folium package looks very good

import folium

#wow it is in Kaggle


# In[28]:



mg.info()


# In[29]:


mg['lat'] = mg['lat'].astype(float)
mg['lon'] = mg['lon'].astype(float)


# In[30]:


max_lat =mg['lat'].max()
max_lon =mg['lon'].max()


# In[31]:




m = folium.Map([max_lat, max_lon], zoom_start=3)
m


# It is not finish. Will come back to plot the missing migrants in a map and see how it looks

