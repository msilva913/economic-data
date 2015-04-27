
# coding: utf-8

# In[9]:

from __future__ import division
import matplotlib.pyplot as plt
import matplotlib.dates as dts
import numpy as np
import runProcs
from scipy.stats import gaussian_kde
import pandas as pd
# get_ipython().magic(u'matplotlib inline')

# This program requires the Penn World Tables data file: pwt81.xlsx
# available at https://pwt.sas.upenn.edu/


# In[10]:

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

# 0.5 Index locator
def findDateIndex(dateStr,fredObj):
    for n,d in enumerate(fredObj.dates):
        if d == dateStr:
            return n


# In[11]:

# 1. Import data
pwt = pd.read_excel('pwt81.xlsx',sheetname='Data')


# In[12]:

# 2. lists of countries, codes, and years
year0 = 1960

countryCodes=[]
countries = []
years = []
for code in pwt['countrycode']:
    if code not in countryCodes:
        countryCodes.append(code)
        
for country in pwt['country']:
    if country == u"Côte d'Ivoire":
        country = u"Cote d'Ivoire"
    if country not in countries:
        countries.append(country)
        
for year in pwt['year']:
    if year not in years:
        years.append(year)

year0= years.index(year0)


# In[13]:

# 3. Create dataset 
incomeDict = {}
incomePcDict = {}
popDict = {}
count=0
for i,code in enumerate(countryCodes):
    income = pwt.loc[pwt['countrycode'] == code]['rgdpe'].values
    pop = pwt.loc[pwt['countrycode'] == code]['pop'].values
    incomePc = income/pop
    if code =='ZWE':
        income = income[0:62]
        incomePc = incomePc[0:62]
        pop = pop[0:62]
    if True not in [np.isnan(x) for x in incomePc[year0:]]:
        incomeDict[countries[i]+' - '+code] = income[year0:].tolist()
        incomePcDict[countries[i]+' - '+code] = incomePc[year0:].tolist()
        popDict[countries[i]+' - '+code] = pop[year0:].tolist()
        count+=1

income = pd.DataFrame(incomeDict,index=years[year0:])
incomePc = pd.DataFrame(incomePcDict,index=years[year0:])
pop = pd.DataFrame(popDict,index=years[year0:])

incomePcLog = np.round(np.log(incomePc),5)
incomePc = np.round(incomePc,5)

# totalPop = pop.sum(axis=1)
# totalIncome = income.sum(axis=1)
# totalIncomePc = totalIncome/totalPop

print count,' countries in the sample.'

incomePc.to_csv('crossCountryIncome.csv',index_label='year')
incomePcLog.to_csv('crossCountryIncomeLog.csv',index_label='year')


# In[14]:

incomePc = pd.read_csv('crossCountryIncome.csv',index_col='year')

names = []
y = []
g = []
for c in incomePc.columns:
    names.append(c)
    income = incomePc[c].iloc[0]
    growth = (incomePc[c].iloc[-1]/incomePc[c].iloc[0])**(1/(len(incomePc[c])-1))-1
    y.append(income/1000)
    g.append(growth*100)


# In[15]:

# 5. Plot for website
data = pd.read_csv('crossCountryIncome.csv',index_col='year')
income60 = data.iloc[0]/1000
growth = 100*((data.iloc[-1]/data.iloc[0])**(1/(len(data.index)-1))-1)

fig = plt.figure(figsize=(10, 6)) 
ax = fig.add_subplot(1,1,1)
colors = ['red','blue','magenta','green']

plt.scatter(income60,growth,s=0.0001)
for i, txt in enumerate(data.columns):
    
    ax.annotate(txt[-3:], (income60[i],growth[i]),fontsize=10,color = colors[np.mod(i,4)])
ax.grid()
# ax.set_xscale('log')
ax.set_xlabel('GDP per capita in 1960\n (thousands of 2005 $ PPP)')
ax.set_ylabel('Real GDP per capita growth\nfrom 1970 to '+str(years[-1])+ ' (%)')
ax.set_xlim([0,20])

fig.tight_layout()
plt.savefig('fig_GDP_GDP_Growth_site.png',bbox_inches='tight')


# In[16]:

#6. Export notebook to python script
runProcs.exportNb('crossCountryIncomeData')


# In[17]:

fig = plt.figure()
ax = fig.add_subplot(1,1,1)

colors = ['red','blue','magenta','green']
ax.scatter(y,g,s=0.0001)

for i, txt in enumerate(names):
    ax.annotate(txt[-3:], (y[i],g[i]),fontsize=7.5,alpha = 0.75,color = colors[np.mod(i,4)])
ax.grid()
# ax.set_xscale('log')
ax.set_xlabel('GDP per capita in 1960\n (thousands of 2005 $ PPP)')
ax.set_ylabel('Real GDP per capita growth\nfrom 1970 to '+str(years[-1])+ ' (%)')
ax.set_xlim([0,20])

fig.tight_layout()
# plt.savefig('fig_GDPpc1960_GDPPpc1960_Growth.png',bbox_inches='tight')


# In[18]:

fig = plt.figure()
ax = fig.add_subplot(1,1,1)

y1960 = incomePc.iloc[years.index(1960)]
yCurrent = incomePc.iloc[-1]

# colors = ['red','blue','magenta','green']
ax.scatter(y1960,yCurrent,s=0.00001)
ax.grid()
ax.set_xscale('log')
ax.set_yscale('log')
ax.set_xlim([10e1,10e4])
ax.set_ylim([10e1,10e4])

x = np.arange(0,100000,1)
line45, = ax.plot(x,x,'k-')
plt.legend([line45],['$45^\circ$'],loc='lower right',fontsize='15')

for i, txt in enumerate(names):
    ax.annotate(txt[-3:], (y1960[i],yCurrent[i]),fontsize=7.5,alpha = 0.75,color = colors[np.mod(i,4)])
ax.set_xlabel('GDP per capita in '+str(years[0])+'\n (thousands of 2005 $ PPP)')
ax.set_ylabel('GDP per capita in '+str(years[-1])+'\n (thousands of 2005 $ PPP)')
fig.tight_layout()
# plt.savefig('fig_GDPpc1960_CDPPpcCurrent.png',bbox_inches='tight')

