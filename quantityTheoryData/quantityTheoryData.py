
# coding: utf-8

# In[1]:

from __future__ import division
# get_ipython().magic(u'matplotlib inline')
import numpy as np
import pandas as pd
import wbdata
import runProcs
import qtyTheoryFunc as qt

# if wbdata fails to load run in the shell: rm -r ~/.cache/wbdata


# In[2]:

# 1. Get the World Bank ISO codes
isoCodes = pd.DataFrame(wbdata.search_countries("",display=False))
isoCodes = isoCodes[['id','name']]
isoCodes = isoCodes.set_index('name')


# In[3]:

# 2. Indices for data series and labels for data frame

indicators = {'FP.CPI.TOTL': 'inflation rate',
              'FM.LBL.MONY.CN': 'money growth', 
              'NY.GDP.MKTP.KD': 'real gdp growth'
              }


# In[4]:

# 3. Create the data frames with raw money, price level, and real gdp data from WB

# 3.1 country groups
countries =  [i['id'] for i in wbdata.get_country(incomelevel=['LIC','MIC','HIC'],display=False)]
countriesH = [i['id'] for i in wbdata.get_country(incomelevel=['HIC'],display=False)]
countriesM = [i['id'] for i in wbdata.get_country(incomelevel=['MIC'],display=False)]
countriesL = [i['id'] for i in wbdata.get_country(incomelevel=['LIC'],display=False)]

# 3.2 data frames
df   = wbdata.get_dataframe(indicators, country=countries,convert_date=True)
hicDf = wbdata.get_dataframe(indicators, country=countriesH,convert_date=True)
micDf = wbdata.get_dataframe(indicators, country=countriesM,convert_date=True)
licDf = wbdata.get_dataframe(indicators, country=countriesL,convert_date=True)


# In[5]:

# 4. Create data sets of money growth, inflation, and real gdp growth
qtyTheoryData, include, dropped = qt.create(dataFrame=df,indicators=indicators,isoCodes=isoCodes,levels=[''],csvFilename='qtyTheoryData',decimals=5)
qtyTheoryDataH, includeH, droppedH = qt.create(dataFrame=hicDf,indicators=indicators,isoCodes=isoCodes,levels=[''],csvFilename='qtyTheoryDataH',decimals=5)
qtyTheoryDataM, includeM, droppedM = qt.create(dataFrame=micDf,indicators=indicators,isoCodes=isoCodes,levels=[''],csvFilename='qtyTheoryDataM',decimals=5)
qtyTheoryDataL, includeL, droppedL = qt.create(dataFrame=licDf,indicators=indicators,isoCodes=isoCodes,levels=[''],csvFilename='qtyTheoryDataL',decimals=5)


# In[6]:

qtyTheoryDataM


# In[7]:

# 6. Verify output 
print 'Number of countries:',len(include),'\n'
print qtyTheoryData.loc['United States']
print qtyTheoryData.loc['Germany']


# In[8]:

# 7. Export notebook to python script
runProcs.exportNb('quantityTheoryData')

