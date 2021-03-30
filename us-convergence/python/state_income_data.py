#!/usr/bin/env python
# coding: utf-8

# In[1]:


import numpy as np
import pandas as pd
import json
import runProcs
from urllib.request import urlopen
import os

import matplotlib.pyplot as plt
plt.style.use('classic')
# get_ipython().run_line_magic('matplotlib', 'inline')


# In[2]:


# 0. Import BEA API key or set manually to variable api_key
try:
    items = os.getcwd().split('/')[:3]
    items.append('bea_api_key.txt')
    path = '/'.join(items)
    with open(path,'r') as api_key_file:
        api_key = api_key_file.readline()

except:
    api_key = None


# In[3]:


# 1. State abbreviations

# 1.1 dictionary:
stateAbbr = {
u'Alabama':u'AL',
u'Alaska *':u'AK',
u'Arizona':u'AZ',
u'Arkansas':u'AR',
u'California':u'CA',
u'Colorado':u'CO',
u'Connecticut':u'CT',
u'Delaware':u'DE',
u'District of Columbia':u'DC',
u'Florida':u'FL',
u'Georgia':u'GA',
u'Hawaii *':u'HI',
u'Idaho':u'ID',
u'Illinois':u'IL',
u'Indiana':u'IN',
u'Iowa':u'IA',
u'Kansas':u'KS',
u'Kentucky':u'KY',
u'Louisiana':u'LA',
u'Maine':u'ME',
u'Maryland':u'MD',
u'Massachusetts':u'MA',
u'Michigan':u'MI',
u'Minnesota':u'MN',
u'Mississippi':u'MS',
u'Missouri':u'MO',
u'Montana':u'MT',
u'Nebraska':u'NE',
u'Nevada':u'NV',
u'New Hampshire':u'NH',
u'New Jersey':u'NJ',
u'New Mexico':u'NM',
u'New York':u'NY',
u'North Carolina':u'NC',
u'North Dakota':u'ND',
u'Ohio':u'OH',
u'Oklahoma':u'OK',
u'Oregon':u'OR',
u'Pennsylvania':u'PA',
u'Rhode Island':u'RI',
u'South Carolina':u'SC',
u'South Dakota':u'SD',
u'Tennessee':u'TN',
u'Texas':u'TX',
u'Utah':u'UT',
u'Vermont':u'VT',
u'Virginia':u'VA',
u'Washington':u'WA',
u'West Virginia':u'WV',
u'Wisconsin':u'WI',
u'Wyoming':u'WY'
}

# 1.2 List of states in the US
stateList = [s for s in stateAbbr]


# In[4]:


# 2. Construct series for price deflator

# 2.1 Obtain data from BEA
gdp_deflator = urlopen('http://apps.bea.gov/api/data/?UserID='+api_key+'&method=GetData&datasetname=NIPA&TableName=T10109&TableID=13&Frequency=A&Year=X&ResultFormat=JSON&')
# result = gdp_deflator.readall().decode('utf-8')
result = gdp_deflator.read().decode('utf-8')
json_response = json.loads(result)


# In[5]:


# 2.2 Construct the data frame for the deflator series
values = []
years = []
for element in json_response['BEAAPI']['Results']['Data']:
#     if element['LineDescription'] == 'Personal consumption expenditures':
    if element['LineDescription'] == 'Gross domestic product':
        years.append(element['TimePeriod'])
        values.append(float(element['DataValue'])/100)

values = np.array([values]).T
data_p = pd.DataFrame(values,index = years,columns = ['price level'])

# 2.3 Display the data
print(data_p)


# In[6]:


# 3. Construct series for per capita income by state, region, and the entire us

# 3.1 Obtain data from BEA
state_y_pc = urlopen('http://apps.bea.gov/api/data/?UserID='+api_key+'&method=GetData&DataSetName=Regional&TableName=SAINC1&LineCode=3&Year=ALL&GeoFips=STATE&ResultFormat=JSON')
# result = state_y_pc.readall().decode('utf-8')
result = state_y_pc.read().decode('utf-8')
json_response = json.loads(result)
# json_response['BEAAPI']['Results']['Data'][0]['GeoName']


# In[7]:


# 3.2 Construct the data frame for the per capita income series

# 3.2.1 Initialize the dataframe
regions = []
years = []
for element in json_response['BEAAPI']['Results']['Data']:
    if element['GeoName'] not in regions:
        regions.append(element['GeoName'])
    if element['TimePeriod'] not in years:
        years.append(element['TimePeriod'])

df = np.zeros([len(years),len(regions)])
data_y = pd.DataFrame(df,index = years,columns = regions)

# 3.2.2 Populate the dataframe with values
for element in json_response['BEAAPI']['Results']['Data']:
    try:
        data_y[element['GeoName']][element['TimePeriod']] = np.round(float(element[u'DataValue'].replace(',',''))/float(data_p.loc[element['TimePeriod']]),2)# real
    except:
        data_y[element['GeoName']][element['TimePeriod']] = np.nan
        
# 3.2.3 Replace the state names in the index with abbreviations
columns=[]
for r in regions:
    if r in stateList:
        columns.append(stateAbbr[r])
    else:
        columns.append(r)
        
data_y.columns=columns

# 3.2.4 Display the data obtained from the BEA
data_y


# In[8]:


# 4. State income data for 1840, 1880, and 1900

# 4.1.1 Import Easterlin's income data
easterlin_data = pd.read_csv('../historic_data/Historical Statistics of the US - Easterlin State Income Data.csv',index_col=0)

# 4.1.2 Import historic CPI data
historic_cpi_data=pd.read_csv('../historic_data/Historical Statistics of the US - cpi.csv',index_col=0)
historic_cpi_data = historic_cpi_data/historic_cpi_data.loc[1929]*float(data_p.loc['1929'])


# In[9]:


# 4.2 Append to data beginning in 1929

# 4.2.1 Construct series for real incomes in 1840, 1880, and 1900
df_1840 = easterlin_data['Income per capita - 1840 - A [cur dollars]']/float(historic_cpi_data.loc[1840])
df_1880 = easterlin_data['Income per capita - 1880 [cur dollars]']/float(historic_cpi_data.loc[1890])
df_1900 = easterlin_data['Income per capita - 1900 [cur dollars]']/float(historic_cpi_data.loc[1900])

# 4.2.2 Put into a DataFrame and concatenate with previous
df = pd.DataFrame({'1840':df_1840,'1880':df_1880,'1900':df_1900}).transpose()
df = pd.concat([data_y,df]).sort_index()


# In[10]:


# 5. Export data to csv
series = df.sort_index()
dropCols = [u'AK', u'HI', u'New England', u'Mideast', u'Great Lakes', u'Plains', u'Southeast', u'Southwest', u'Rocky Mountain', u'Far West']
for c in dropCols:
    series = series.drop([c],axis=1)

series.to_csv('../csv/state_income_data.csv',na_rep='NaN')


# In[11]:


# 6. Export notebook to .py
runProcs.exportNb('state_income_data')

