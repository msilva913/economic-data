#!/usr/bin/env python
# coding: utf-8

# In[1]:


import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import runProcs
import os
plt.style.use('classic')
# get_ipython().run_line_magic('matplotlib', 'inline')


# # Cross Country Income Data
# 
# This program extracts particular series from the Penn World Tables (PWT). Data and documentation for the PWT are available at https://pwt.sas.upenn.edu/. For additional reference see the article "The Next Generation of the Penn World Table" by Feenstra, Inklaar, and Timmer in the October 2015 issue of the *American Economic Review* (https://www.aeaweb.org/articles?id=10.1257/aer.20130954)
# 
# ## Import data and manage

# In[2]:


# Set the current value of the PWT data file
current_pwt_file = 'pwt100.xlsx'


# In[3]:


# Import data from local source or download if not present
if os.path.exists('../xslx/pwt100.xlsx'):
    pwt = pd.read_excel('../xslx/'+current_pwt_file,sheet_name='Data',index_col=3,parse_dates=True)
else:
    pwt = pd.read_excel('https://www.rug.nl/ggdc/docs/'+current_pwt_file,sheet_name='Data',index_col=3,parse_dates=True)


# In[4]:


# Replace Côte d'Ivoire with Cote d'Ivoire
pwt['country'] = pwt['country'].str.replace(u"Côte d'Ivoire",u"Cote d'Ivoire")

# Merge country name and code
pwt['country'] = pwt['country']+' - '+pwt['countrycode']

# Create hierarchical index
pwt = pwt.set_index(['country',pwt.index])

# Display new DataFrame
pwt


# ## Contstruct data sets

# In[5]:


# Define a function that constructs data sets
def create_data_set(year0,pwtCode,per_capita,per_worker,file_name):
    
    year0 = str(year0)
    
    if per_capita:
        data = pwt[pwtCode]/pwt['pop']
        
    elif per_worker:
        data = pwt[pwtCode]/pwt['emp']
        
    else:
        data = pwt[pwtCode]
        
    data = data.unstack(level='country').loc[year0:].dropna(axis=1)
    
    data.to_csv(file_name)


# ### GDP data

# In[6]:


# GDP (output-side, constant prices across countries; PWT code: cgdpo)
create_data_set(year0=1960,pwtCode='cgdpe',per_capita=False,per_worker=False,file_name='../csv/cross_country_gdp.csv')

# GDP per capita (output-side, constant prices across countries; PWT code: cgdpo)
create_data_set(year0=1960,pwtCode='cgdpe',per_capita=True,per_worker=False,file_name='../csv/cross_country_gdp_per_capita.csv')

# GDP per worker (output-side, constant prices across countries; PWT code: cgdpo)
create_data_set(year0=1960,pwtCode='cgdpe',per_capita=False,per_worker=True,file_name='../csv/cross_country_gdp_per_worker.csv')


# ### Consumption data

# In[7]:


# Consumption (constant prices across countries; PWT code: ccon)
create_data_set(year0=1960,pwtCode='ccon',per_capita=False,per_worker=False,file_name='../csv/cross_country_consumption.csv')

# Consumption per capita (constant prices across countries; PWT code: ccon)
create_data_set(year0=1960,pwtCode='ccon',per_capita=True,per_worker=False,file_name='../csv/cross_country_consumption_per_capita.csv')

# Consumption per worker (constant prices across countries; PWT code: ccon)
create_data_set(year0=1960,pwtCode='ccon',per_capita=False,per_worker=True,file_name='../csv/cross_country_consumption_per_worker.csv')


# ### Physical capital data

# In[8]:


# Physical capital (constant prices across countries; PWT code: cn)
create_data_set(year0=1960,pwtCode='cn',per_capita=False,per_worker=False,file_name='../csv/cross_country_physical_capital.csv')

# Physical capital (constant prices across countries; PWT code: cn)
create_data_set(year0=1960,pwtCode='cn',per_capita=True,per_worker=False,file_name='../csv/cross_country_physical_capital_per_capita.csv')

# Physical capital (constant prices across countries; PWT code: cn)
create_data_set(year0=1960,pwtCode='cn',per_capita=False,per_worker=True,file_name='../csv/cross_country_physical_capital_per_worker.csv')


# ### Human capital data

# In[9]:


# Human capital (index; PWT code: hc)
create_data_set(year0=1960,pwtCode='hc',per_capita=False,per_worker=False,file_name='../csv/cross_country_human_capital.csv')

# Human capital per capita (index; PWT code: hc)
create_data_set(year0=1960,pwtCode='hc',per_capita=True,per_worker=False,file_name='../csv/cross_country_human_capital_per_capita.csv')

# Human capital per worker (index; PWT code: hc)
create_data_set(year0=1960,pwtCode='hc',per_capita=False,per_worker=True,file_name='../csv/cross_country_human_capital_per_worker.csv')


# ### Other aggregate series

# In[10]:


# Employment (number of persons; PWT code: emp
create_data_set(year0=1960,pwtCode='emp',per_capita=False,per_worker=False,file_name='../csv/cross_country_employed.csv')

# Hours worked (average annual hours workerd by workers; PWT code: avh)
create_data_set(year0=1960,pwtCode='avh',per_capita=False,per_worker=False,file_name='../csv/cross_country_hours.csv')

# Population (PWT code: pop)
popluation = create_data_set(year0=1960,pwtCode='pop',per_capita=False,per_worker=False,file_name='../csv/cross_country_population.csv')

# Saving rate (share of gross capital formation; PWT code: csh_i)
savingRate = create_data_set(year0=1960,pwtCode='csh_i',per_capita=False,per_worker=False,file_name='../csv/cross_country_saving_rate.csv')

# Labor share of income (PWT code: labsh)
create_data_set(year0=1960,pwtCode='labsh',per_capita=False,per_worker=False,file_name='../csv/cross_country_labor_share.csv')

# Aggregate capital depreciation (PWT code: delta)
create_data_set(year0=1960,pwtCode='delta',per_capita=False,per_worker=False,file_name='../csv/cross_country_depreciation_rate.csv')


# ## Plot for website

# In[11]:


# Load data
df = pd.read_csv('../csv/cross_country_gdp_per_capita.csv',index_col='year',parse_dates=True)
income60 = df.iloc[0]/1000
growth = 100*((df.iloc[-1]/df.iloc[0])**(1/(len(df.index)-1))-1)

# Construct plot
fig = plt.figure(figsize=(10, 6)) 
ax = fig.add_subplot(1,1,1)
colors = ['red','blue','magenta','green']

plt.scatter(income60,growth,s=0.0001)
for i, txt in enumerate(df.columns):
    
    ax.annotate(txt[-3:], (income60[i],growth[i]),fontsize=10,color = colors[np.mod(i,4)])
ax.grid()

ax.set_xlabel('GDP per capita in 1960\n (thousands of 2011 $ PPP)')
ax.set_ylabel('Real GDP per capita growth\nfrom 1970 to '+str(df.index[0].year)+ ' (%)')
xlim = ax.get_xlim()
ax.set_xlim([0,xlim[1]])

fig.tight_layout()

# Save image
plt.savefig('../png/fig_GDP_GDP_Growth_site.png',bbox_inches='tight')


# In[12]:


# Export notebook to python script
runProcs.exportNb('cross_country_income_data')

