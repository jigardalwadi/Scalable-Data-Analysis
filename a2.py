
# coding: utf-8

# In[2]:


import pandas as pd
import numpy as np
import sys
import os
sys.path.append("..") # Adds higher directory to python modules path.  Use to run this example locallay without a global pip install.

from mapboxgl.viz import *
from mapboxgl.utils import df_to_geojson, create_radius_stops, scale_between, df_to_hexbin, hexbin
from mapboxgl.colors import create_color_stops


# In[3]:


import csv 
df = pd.read_csv("2015_Street_Tree_Census_-_Tree_Data.csv", low_memory=False)


# In[4]:


("Q1 Starts here")


# In[5]:


df = df.head(15000)
df


# In[3]:


acces_token = os.getenv("MAPBOX_ACCESS_TOKEN")


# In[4]:


#data = df_to_geojson(df, 
 #                    properties=['Avg Medicare Payments', 'Avg Covered Charges'],
  #                   precision=4)
data = df_to_geojson(df, properties=["status"],lat='latitude', lon='longitude', precision=None)


# In[187]:


viz = CircleViz(data,
                color_property=None,
               # color_stops=None,
                color_type="interval",
                opacity=0.8,
                label_property=None,
                div_id='map',
                height='500px',
                style_url="mapbox://styles/mapbox/light-v9?optimize=true",
                width='100%',
                zoom=10,
                access_token=acces_token)
#viz = CircleViz(data, access_token=acces_token, height='400px')
viz


# In[5]:


# Jenks natural breaks classification for example.
# Slow version - does not require C bindings
# For fast version, see pip install -e "git+https://github.com/perrygeo/jenks.git#egg=jenks"
import json
from pprint import pprint as pp

def jenks_matrices_init(data, n_classes):
    #fill the matrices with data+1 arrays of n_classes 0s
    lower_class_limits = []
    variance_combinations = []
    for i in range(0, len(data)+1):
        temp1 = []
        temp2 = []
        for j in range(0, n_classes+1):
            temp1.append(0.)
            temp2.append(0.)
        lower_class_limits.append(temp1)
        variance_combinations.append(temp2)

    inf = float('inf')
    for i in range(1, n_classes+1):
        lower_class_limits[1][i] = 1.
        variance_combinations[1][i] = 0.
        for j in range(2, len(data)+1):
            variance_combinations[j][i] = inf

    return lower_class_limits, variance_combinations

def jenks_matrices(data, n_classes):
    lower_class_limits, variance_combinations = jenks_matrices_init(data, n_classes)

    variance = 0.0
    for l in range(2, len(data)+1):
        sum = 0.0
        sum_squares = 0.0
        w = 0.0
        for m in range(1, l+1):
            # `III` originally
            lower_class_limit = l - m + 1
            val = data[lower_class_limit-1]

            # here we're estimating variance for each potential classing
            # of the data, for each potential number of classes. `w`
            # is the number of data points considered so far.
            w += 1

            # increase the current sum and sum-of-squares
            sum += val
            sum_squares += val * val

            # the variance at this point in the sequence is the difference
            # between the sum of squares and the total x 2, over the number
            # of samples.
            variance = sum_squares - (sum * sum) / w

            i4 = lower_class_limit - 1

            if i4 != 0:
                for j in range(2, n_classes+1):
                    if variance_combinations[l][j] >= (variance + variance_combinations[i4][j - 1]):
                        lower_class_limits[l][j] = lower_class_limit
                        variance_combinations[l][j] = variance + variance_combinations[i4][j - 1]

        lower_class_limits[l][1] = 1.
        variance_combinations[l][1] = variance

    return lower_class_limits, variance_combinations

def get_jenks_breaks(data, lower_class_limits, n_classes):
    k = len(data) - 1
    kclass = [0.] * (n_classes+1)
    countNum = n_classes

    kclass[n_classes] = data[len(data) - 1]
    kclass[0] = data[0]

    while countNum > 1:
        elt = int(lower_class_limits[k][countNum] - 2)
        kclass[countNum - 1] = data[elt]
        k = int(lower_class_limits[k][countNum] - 1)
        countNum -= 1

    return kclass

def jenks(data, n_classes):
    if n_classes > len(data): return

    data.sort()

    lower_class_limits, _ = jenks_matrices(data, n_classes)

    return get_jenks_breaks(data, lower_class_limits, n_classes)


# In[189]:


breaks = jenks(df['tree_id'].tolist(), 8)
color_stops = create_color_stops(breaks, colors='YlGnBu')
color_stops


# In[190]:


#Q1 final answer
#I have took only 15000 rows as it was taking too much time for processinf


# In[191]:


#breaks = jenks(df['tree_dbh'].tolist(), 1 )
#color_stops = create_color_stops(breaks, colors='YlGnBu')
#color_stops
viz.color_property = "tree_id"
viz.color_stops = color_stops
viz.center = (-74, 40.7)
viz.zoom = 8.9
viz.show()


# In[115]:


#Q2 Starts


# In[116]:


# filter the dataset on column stump_diam 


# In[202]:


df = pd.read_csv("2015_Street_Tree_Census_-_Tree_Data.csv", low_memory=False)


# In[203]:


df.status.unique()


# In[204]:


df = df[df.status == 'Stump']


# In[269]:


df


# In[272]:


data = df_to_geojson(df, properties=["status"],lat='latitude', lon='longitude', precision=None)


# In[271]:


breaks = jenks(df['stump_diam'].tolist(), 8)
color_stops = create_color_stops(breaks, colors='YlGnBu')


# In[208]:


# the answer for Q2


# In[273]:


viz = CircleViz(data,
                color_property=None,
                color_stops=color_stops,
                color_type="interval",
                opacity=0.8,
                label_property=None,
                div_id='map',
                height='500px',
                style_url="mapbox://styles/mapbox/light-v9?optimize=true",
                width='100%',
                zoom=8.5,
                center=[-74,40.6],
                access_token=acces_token)
#viz = CircleViz(data, access_token=acces_token, height='400px')
viz.show()


# In[331]:


df.status.count()
#Out of all exactly 50000 are stump


# In[210]:


#Q3 starts


# In[8]:


df = pd.read_csv("ny_trees_50000.csv", low_memory=False)


# In[9]:


df


# In[11]:


items_counts = df['spc_common'].value_counts()
max_item = items_counts.max()
max_item


# In[12]:


items_counts.head(8)


# In[13]:


df1 = df.loc[df['spc_common'].isin(['London planetree','honeylocust','Callery pear','pin oak','Norway maple','Japanese zelkova','cherry','littleleaf linden'])]
df1


# In[318]:


def spc_new (row):
   if row['spc_common'] == 'London planetree' :
      return 0
   if row['spc_common'] == 'honeylocust' :
      return 5
   if row['spc_common'] == 'Callery pear' :
      return 10
   if row['spc_common'] == 'pin oak' :
      return 15
   if row['spc_common'] == 'Norway maple' :
      return 20
   if row['spc_common'] == 'Japanese zelkova' :
      return 25
   if row['spc_common'] == 'cherry' :
      return 30
   if row['spc_common'] == 'littleleaf linden' :
      return 35
   return 'Other'
#['London planetree','honeylocust','Callery pear','pin oak','Norway maple','Japanese zelkova','cherry','littleleaf linden'])]


# In[319]:


#df1['new_spc'] =
df2 = df1.apply (lambda row: spc_new (row),axis=1)
#df2
df1['new_spc'] = df2


# In[320]:


# I have added one column based on the spc_common. As I wanted to show the breaks based on the spa_common. Breaks takes only integer values so I have added a column.
df1


# In[321]:


data1 = df_to_geojson(df1, properties=["spc_common","status","new_spc",'tree_id'],lat='latitude', lon='longitude', precision=None)


# In[322]:


viz = CircleViz(data1, access_token=acces_token, height='400px')


# In[323]:


breaks = jenks(df1['new_spc'].tolist(), 7)
color_stops = create_color_stops(breaks, colors="Paired")
color_stops


# In[324]:


#viz2 = CircleViz(data1, access_token=acces_token, color_property='tree_id',
 #                color_stops=color_stops, color_type='categorical',center=[-95, 40], zoom=3)
#viz2.show()
viz.color_property = "new_spc"
viz.color_stops = color_stops
viz.center = (-74, 40.8)
viz.zoom = 8.5

viz.show()
#print('Q3 final answer')


# In[345]:


#Q4


# In[6]:


df4 = pd.read_csv("ny_trees_all.csv", low_memory=False)
df4


# In[326]:


#data2 = df_to_geojson(df4, properties=["spc_common","status",'tree_id'],lat='latitude', lon='longitude', precision=None)


# In[9]:


data2 = df_to_hexbin(df4, lat='latitude', lon='longitude', radius=600)
data2[1]


# In[328]:


li = np.linspace(0,data2[1],8)
color_stops = create_color_stops(li, colors="Greens")
color_stops


# In[329]:


viz1 = HexbinViz(data2[0], access_token=acces_token, height='400px')


# In[330]:


viz1.color_property ="count"
viz1.color_stops = color_stops
viz1.center = (-74, 40.8)
viz1.zoom = 8.5


viz1.show()


# In[ ]:


#Q4 final answer

