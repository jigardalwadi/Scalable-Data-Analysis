
# coding: utf-8

# In[5]:


import pandas


# In[2]:


import numpy as np


# In[3]:


import pandas as pd


# In[52]:


print("Jigar Dalwadi")
print("01684802")


# In[4]:


import csv


# In[10]:


df = pd.read_csv("property-assessment.csv", low_memory=False)


# In[11]:


df


# In[18]:


len(df)


# In[42]:


# Q1


# In[37]:


id = df["AV_TOTAL"]


# In[38]:


id


# In[40]:


df['AV_TOTAL'].argmax()


# In[36]:


df.loc[df['AV_TOTAL'].idxmax()]


# In[48]:


index = df['AV_TOTAL'].idxmax()
index


# In[10]:


#Answer for Q1
value = df['AV_TOTAL'].nlargest(1)
value


# In[41]:


# Q2


# In[50]:


year = df['YR_BUILT']
year


# In[11]:


#Answer for Q2 max year
maxyear = df['YR_BUILT'].nlargest(1)


# In[12]:


minyear = df['YR_BUILT'].nsmallest(1)


# In[13]:


maxyear


# In[14]:


minyear


# In[15]:


#https://stackoverflow.com/questions/18172851/deleting-dataframe-row-in-pandas-based-on-column-value
year = df[df.YR_BUILT != 0]


# In[16]:


year = df.YR_BUILT[df.YR_BUILT != 0]


# In[17]:


maxyear


# In[22]:


minyear


# In[21]:


#Answer for Q2 min year
minyear = df.YR_BUILT[df.YR_BUILT != 0].nsmallest(1)


# In[23]:


#Answer for Q2 meann of the years without 0
meanyear = df.YR_BUILT[df.YR_BUILT != 0 ].mean()


# In[25]:


meanyear


# In[27]:


#Answer for Q2 meann of the years with 0
meanyear1 = df.YR_BUILT.mean()
meanyear1


# In[12]:


lu = df['LU'] 


# In[38]:


lu


# In[86]:


lu = df['LU'].unique()


# In[87]:


lu


# In[40]:


# Q3


# In[13]:


# Q3 Selecting the single residentes 
lu = df[df['LU'] == "R1"]


# In[40]:


lu


# In[150]:


#https://stackoverflow.com/questions/14733871/multi-index-sorting-in-pandas
#Sorting all single residentes by land value
grp = lu.sort_values(by=('AV_LAND'), ascending=False)


# In[151]:


grp 


# In[152]:


# Q3 Getting top 5 out of the list
grp = grp.head(n=5)


# In[153]:


grp


# In[154]:


# Q3 count of the streets from the top five
grp1 = grp['ST_NAME'].value_counts()


# In[155]:


grp1


# In[158]:


# Q3 Sorting the top 5 according to most occurence of the street
grpfinal = grp.sort_values(by=('ST_NAME'), ascending=False)


# In[159]:


grpfinal


# In[14]:


#4
lu


# In[39]:


# Q4 


# In[15]:


#Tax bill amount based on total assessed value multiplied by the tax rate
grostax = lu['GROSS_TAX'].sum()


# In[16]:


grostax


# In[17]:


#Total assessed value for property
avtotal = lu['AV_TOTAL'].sum()


# In[18]:


avtotal


# In[21]:


meadian = grostax/avtotal
meadian


# In[31]:


# Q4 Meadian for single residents tax rate
print("#current rate for tax is, per 1000$ property, the tax is 10.59$ which means gross total should be 1010.59")#https://www.boston.gov/departments/assessing/how-we-tax-your-property
print("meadian from the site is")
1010.59/1000


# In[36]:


print("Our outcome is higher then the outcome from the site")
print("The difference between our outcome and sites outcome in percentage is")
(1.059-1.010)


# In[38]:


# Q4 Reason 
print("I think that this miner difference is because of the year it built. the rate is seems higher in the old build buldings. The buildings which are not renewed or renewed early have higher tax rates. So at the time of average it's getting higher than it should be")


# In[167]:


#per 1000$ property the tax is 1.059


# In[225]:


#Q5 sorting acording to Street name
sort= lu.sort_values(by=('ST_NAME'), ascending=False)


# In[224]:


#print(sort.groupby(['ST_NAME']))


# In[262]:


# Getting count to get aware about streets below 20 residdents
count = lu['ST_NAME'].value_counts() 
count


# In[244]:


# getting count of streets with atleast 20 residents
x = count.where(count > 20).dropna()
len(x)


# In[271]:


# Q5 grouing according to avg tax 
lu.groupby(['ST_NAME'])['GROSS_TAX'].mean().where(count > 20).dropna()


# In[268]:


# Q5 another method 
lu.groupby('ST_NAME')['GROSS_TAX'].agg(['mean','count']).where(count > 20).dropna()


# In[261]:




