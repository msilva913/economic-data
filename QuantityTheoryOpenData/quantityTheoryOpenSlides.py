
# coding: utf-8

# In[1]:

from __future__ import division
# get_ipython().magic(u'matplotlib inline')
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as dts
import pandas as pd
import wbdata
import runProcs
from scipy import stats
import qtyTheoryFunc as qt

# if wbdata fails to load run in the shell: rm -r ~/.cache/wbdata


# In[2]:

# 0. Preliminaries

# 0.1 general plot settings

font = {'weight' : 'bold',
        'size'   : 15}
axes={'labelweight' : 'bold'}
plt.rc('font', **font)
plt.rc('axes', **axes)
plt.rcParams['xtick.major.pad']='8'
plt.rcParams['ytick.major.pad']='8'


# In[3]:

# 1. Get the World Bank ISO codes
isoCodes = pd.DataFrame(wbdata.search_countries("",display=False))
isoCodes = isoCodes[['id','name']]
isoCodes = isoCodes.set_index('name')


# In[4]:

# 2. Indices for data series and labels for data frame

indicators = {'PA.NUS.FCRF':'exchange rate growth',
              'FP.CPI.TOTL': 'inflation rate',
              'FR.INR.LEND': 'interest rate',
              'FM.LBL.MONY.CN': 'money growth', 
              'NY.GDP.MKTP.KD': 'real gdp growth'
              }


# In[5]:

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


# In[6]:

# 4. Create data sets of money growth, inflation, and real gdp growth
qtyTheoryData, include, dropped = qt.create(dataFrame=df,indicators=indicators,isoCodes=isoCodes,levels=['interest rate'],csvFilename='qtyTheoryOpenData',decimals=5)
qtyTheoryDataH, includeH, droppedH = qt.create(dataFrame=hicDf,indicators=indicators,isoCodes=isoCodes,levels=['interest rate'],csvFilename='qtyTheoryOpenDataH',decimals=5)
qtyTheoryDataM, includeM, droppedM = qt.create(dataFrame=micDf,indicators=indicators,isoCodes=isoCodes,levels=['interest rate'],csvFilename='qtyTheoryOpenDataM',decimals=5)
qtyTheoryDataL, includeL, droppedL = qt.create(dataFrame=licDf,indicators=indicators,isoCodes=isoCodes,levels=['interest rate'],csvFilename='qtyTheoryOpenDataL',decimals=5)


# In[7]:

qtyTheoryData['interest rate'] = qtyTheoryData['interest rate']/100
qtyTheoryDataL['interest rate'] = qtyTheoryDataL['interest rate']/100 
qtyTheoryDataM['interest rate'] = qtyTheoryDataM['interest rate']/100
qtyTheoryDataH['interest rate'] = qtyTheoryDataH['interest rate']/100


# In[8]:

# 5. Verify output for US
print 'Number of countries:',len(include),'\n'
print qtyTheoryData.loc['United States']
# print qtyTheoryDataH.loc['Germany']


# In[9]:

# 6. Plots.

# 6.1 Money growth and currency depreciation

xmin = -0.2
xmax = 1.4
ymin = -.2
ymax = 1.4

x45 = np.arange(xmin,xmax,0.001)
y45 = x45 #- np.mean(qtyTheoryData['money growth'])

fig = plt.figure()

ax1 = fig.add_subplot(1, 1, 1)
ax1.plot(x45,y45)
ax1.plot(qtyTheoryDataH['money growth'] - qtyTheoryDataH['money growth']['United States'],qtyTheoryDataH['exchange rate growth'],'bo')
ax1.plot(qtyTheoryDataM['money growth'] - qtyTheoryDataH['money growth']['United States'],qtyTheoryDataM['exchange rate growth'],'gs')
ax1.plot(qtyTheoryDataL['money growth'] - qtyTheoryDataH['money growth']['United States'],qtyTheoryDataL['exchange rate growth'],'r^')
plt.grid(True)
# ax1.set_title('',fontsize=15)
ax1.set_xlabel('money growth differential')
ax1.set_ylabel('depreciation')
plt.legend(['$45^\circ$'],loc='lower right',fontsize='15')
plt.axis([xmin,xmax,ymin,ymax])

plt.tight_layout()
plt.savefig('fig_depreciationMoneyGrowth.png',bbox_inches='tight',dpi=120)


# In[10]:

# 6.2 Interest differentials versus inflation differentials

xmin = -0.2
xmax = 1.4
ymin = -.2
ymax = 1.4

x45 = np.arange(xmin,xmax,0.001)
y45 = x45 #- np.mean(qtyTheoryData['money growth'])

fig = plt.figure()

ax1 = fig.add_subplot(1, 1, 1)
ax1.plot(x45,y45)
ax1.plot(qtyTheoryDataH['inflation rate'] - qtyTheoryData['inflation rate']['United States'],100*(qtyTheoryDataH['interest rate'] - qtyTheoryData['interest rate']['United States']),'bo')
ax1.plot(qtyTheoryDataM['inflation rate'] - qtyTheoryData['inflation rate']['United States'],100*(qtyTheoryDataM['interest rate'] - qtyTheoryData['interest rate']['United States']),'gs')
ax1.plot(qtyTheoryDataL['inflation rate'] - qtyTheoryData['inflation rate']['United States'],100*(qtyTheoryDataL['interest rate'] - qtyTheoryData['interest rate']['United States']),'r^')
plt.grid(True)
# ax1.set_title('',fontsize=15)
ax1.set_xlabel('inflation differential')
ax1.set_ylabel('interest differential')
plt.legend(['$45^\circ$'],loc='lower right',fontsize='15')
plt.axis([xmin,xmax,ymin,ymax])

plt.tight_layout()
plt.savefig('fig_interestInflation.png',bbox_inches='tight',dpi=120)


# In[11]:

# 6.3 Inflation and currency depreciation

xmin = -0.2
xmax = 1.4
ymin = -.2
ymax = 1.4

x45 = np.arange(xmin,xmax,0.001)
y45 = x45 #- np.mean(qtyTheoryData['money growth'])

fig = plt.figure()

ax1 = fig.add_subplot(1, 1, 1)
ax1.plot(x45,y45)
ax1.plot(qtyTheoryDataH['inflation rate'] - qtyTheoryDataH['inflation rate']['United States'],qtyTheoryDataH['exchange rate growth'],'bo')
ax1.plot(qtyTheoryDataM['inflation rate'] - qtyTheoryDataH['inflation rate']['United States'],qtyTheoryDataM['exchange rate growth'],'gs')
ax1.plot(qtyTheoryDataL['inflation rate'] - qtyTheoryDataH['inflation rate']['United States'],qtyTheoryDataL['exchange rate growth'],'r^')
plt.grid(True)
# ax1.set_title('',fontsize=15)
ax1.set_xlabel('inflation differential')
ax1.set_ylabel('depreciation')
plt.legend(['$45^\circ$'],loc='lower right',fontsize='15')
plt.axis([xmin,xmax,ymin,ymax])

plt.tight_layout()
plt.savefig('fig_depreciationinflation.png',bbox_inches='tight',dpi=120)


# In[12]:

# 11. Export notebook to python script
runProcs.exportNb('quantityTheoryOpen')

