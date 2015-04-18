
# coding: utf-8

# In[ ]:

from __future__ import division,unicode_literals
# get_ipython().magic(u'matplotlib inline')
import numpy as np
import pandas as pd
import json
import runProcs
from urllib2 import urlopen


# In[ ]:

# 0. State abbreviations

# 0.1 dictionary:
stateAbbr = {
u'Alabama':u'AL',
u'Alaska':u'AK',
u'Arizona':u'AZ',
u'Arkansas':u'AR',
u'California':u'CA',
u'Colorado':u'CO',
u'Connecticut':u'CT',
u'Delaware':u'DE',
u'District of Columbia':u'DC',
u'Florida':u'FL',
u'Georgia':u'GA',
u'Hawaii':u'HI',
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

# 0.2 List of states in the US
stateList = [s for s in stateAbbr]


# In[ ]:

# 1. Construct series for price deflator

# 1.1 Obtain data from BEA
gdpDeflator = urlopen('http://bea.gov/api/data/?UserID=3EDEAA66-4B2B-4926-83C9-FD2089747A5B&method=GetData&datasetname=NIPA&TableID=13&Frequency=A&Year=X&ResultFormat=JSON&')
result = gdpDeflator.read()
jsonResponse = json.loads(result)


# In[ ]:

# 1.2 Construct the data frame for the deflator series
values = []
years = []
for element in jsonResponse['BEAAPI']['Results']['Data']:
#     if element['LineDescription'] == 'Personal consumption expenditures':
    if element['LineDescription'] == 'Gross domestic product':
        years.append(element['TimePeriod'])
        values.append(float(element['DataValue'])/100)

values = np.array([values]).T
dataP = pd.DataFrame(values,index = years,columns = ['price level'])

# 1.3 Display the data
print dataP


# In[ ]:

# 2. Construct series for per capita income by state, region, and the entire us

# 2.1 Obtain data from BEA
stateYpc = urlopen('http://bea.gov/api/data/?UserID=3EDEAA66-4B2B-4926-83C9-FD2089747A5B&method=GetData&datasetname=RegionalData&KeyCode=PCPI_SI&Year=ALL&GeoFips=STATE&ResultFormat=JSON&')
result = stateYpc.read()
jsonResponse = json.loads(result)
# jsonResponse['BEAAPI']['Results']['Data'][0]['GeoName']


# In[ ]:

# 2.2 Construct the data frame for the per capita income series


# 2.2.1 Initialize the dataframe
regions = []
years = []
for element in jsonResponse['BEAAPI']['Results']['Data']:
    if element['GeoName'] not in regions:
        regions.append(element['GeoName'])
    if element['TimePeriod'] not in years:
        years.append(element['TimePeriod'])

df = np.zeros([len(years),len(regions)])
dataY = pd.DataFrame(df,index = years,columns = regions)
# 2.2.2 Populate the dataframe with values
for element in jsonResponse['BEAAPI']['Results']['Data']:
    try:
        dataY[element['GeoName']][element['TimePeriod']] = np.round(float(element[u'DataValue'])/float(dataP.loc[element['TimePeriod']]),2)# real
    except:
        dataY[element['GeoName']][element['TimePeriod']] = np.nan
        
# 2.2.3 Replace the state names in the index with abbreviations
columns=[]
for r in regions:
    if r in stateList:
        columns.append(stateAbbr[r])
    else:
        columns.append(r)
        
dataY.columns=columns

# 2.2.4 Display the data
dataY


# In[ ]:

# 3. Export data to csv
series = dataY
dropCols = [u'AK', u'HI', u'New England', u'Mideast', u'Great Lakes', u'Plains', u'Southeast', u'Southwest', u'Rocky Mountain', u'Far West']
for c in dropCols:
    series = series.drop([c],axis=1)

series.to_csv('stateIncomeData.csv',na_rep='NaN')


# In[ ]:

# 4. Export notebook to .py
runProcs.exportNb('stateIncomeData')

