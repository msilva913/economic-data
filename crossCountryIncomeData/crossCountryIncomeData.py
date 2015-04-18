
# coding: utf-8

# In[1]:

from __future__ import division
import matplotlib.pyplot as plt
import matplotlib.dates as dts
import numpy as np
import runProcs
import wbdata
import pandas as pd
# get_ipython().magic(u'matplotlib inline')


# In[2]:

# 0. Setup

# 0.1 general plot settings

font = {'weight' : 'bold',
        'size'   : 15}
plt.rc('font', **font)
plt.rcParams['xtick.major.pad']='8'
plt.rcParams['ytick.major.pad']='8'


# 0.2 Formatter for inserting commas in y axis labels with magnitudes in the thousands

def func(x, pos):  # formatter function takes tick label and tick position
   s = '{:0,d}'.format(int(x))
   return s

y_format = plt.FuncFormatter(func)  # make formatter

# 0.3 format the x axis ticksticks
years2,years4,years5,years10,years15= dts.YearLocator(2),dts.YearLocator(4),dts.YearLocator(5),dts.YearLocator(10),dts.YearLocator(15)


# 0.4 y label locator for vertical axes plotting gdp
majorLocator_y   = plt.MultipleLocator(3)
majorLocator_shares   = plt.MultipleLocator(0.2)


# In[3]:

# 1. Get the World Bank ISO codes
isoCodes = pd.DataFrame(wbdata.search_countries("",display=False))
isoCodes = isoCodes[['id','name']]
isoCodes = isoCodes.set_index('name')


# In[4]:

# 2. Indices for data series and labels for data frame

indicators = {'NY.GDP.PCAP.KD':'GDP per capita (constant 2005 US$)'
              }


# In[5]:

# 3.1 country groups
countries =  [i['id'] for i in wbdata.get_country(incomelevel=['LIC','MIC','HIC'],display=False)]
# countriesH = [i['id'] for i in wbdata.get_country(incomelevel=['HIC'],display=False)]
# countriesM = [i['id'] for i in wbdata.get_country(incomelevel=['MIC'],display=False)]
# countriesL = [i['id'] for i in wbdata.get_country(incomelevel=['LIC'],display=False)]

# 3.2 data frames
df   = wbdata.get_dataframe(indicators, country=countries,convert_date=True)


# In[6]:

# 4. Create the data sets
crossCountryIncome = pd.DataFrame([])
crossCountryIncomeLog = pd.DataFrame([])
sampleN=0
t0 = 10
for country, newDf in df.groupby(level=0):
    newDf = newDf.reset_index()
    newDf = newDf.set_index('date')
    tempSeriesLog = pd.Series(np.log(newDf['GDP per capita (constant 2005 US$)']/1000))
    tempSeries = pd.Series(newDf['GDP per capita (constant 2005 US$)']/1000)
    if not np.isnan(tempSeries.sort_index().iloc[t0]) and not np.isnan(tempSeries.sort_index().iloc[-2]):
        crossCountryIncomeLog[isoCodes.loc[country][0]+' - '+country] = tempSeriesLog
        crossCountryIncome[isoCodes.loc[country][0]+' - '+country] = tempSeries
        sampleN+=1
print 'countries in sample: ',sampleN
crossCountryIncomeLog = crossCountryIncomeLog.sort_index()
crossCountryIncome = crossCountryIncome.sort_index()

crossCountryIncomeLog = crossCountryIncomeLog.iloc[t0:-1]
crossCountryIncome = crossCountryIncome.iloc[t0:-1]
    
crossCountryIncomeLog.to_csv('crossCountryIncomeLog.csv',index_label='date')
crossCountryIncome.to_csv('crossCountryIncome.csv',index_label='date')


# In[7]:

# 5. Plot for website

data = pd.read_csv('crossCountryIncome.csv',index_col='date')
income70 = data.iloc[0]
growth = 100*((data.iloc[-1]/data.iloc[0])**(1/(len(data.index)-1))-1)

fig = plt.figure(figsize=(10, 6)) 
ax = fig.add_subplot(1,1,1)
colors = ['red','blue','magenta','green']

plt.scatter(income70,growth,s=0.0001)
for i, txt in enumerate(data.columns):
    
    ax.annotate(txt[0:3], (income70[i],growth[i]),fontsize=10,color = colors[np.mod(i,4)])
ax.grid()
# ax.set_xscale('log')
ax.set_xlabel('GDP per capita 1970 (2005 $)')
ax.set_ylabel('Real GDP per capita growth\nfrom 1970 to '+str(data.index[-1][0:4]))

fig.tight_layout()
# plt.savefig('fig_GDP_GDP_Growth_site.png',bbox_inches='tight')


# In[8]:

#6. Export notebook to python script
runProcs.exportNb('crossCountryIncomeData')

