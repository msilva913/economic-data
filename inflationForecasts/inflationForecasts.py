
# coding: utf-8

# In[1]:

from __future__ import division
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as dts
import pandas as pd
from fredpy import series, window_equalize, quickplot
import datetime,dateutil,urllib,runProcs
import requests
# get_ipython().magic('matplotlib inline')


# In[2]:

# 1. Import the most recent inflation forecast data from the Philadelphia Fed, Survey of Professional Forecasters

url = "https://www.philadelphiafed.org/-/media/research-and-data/real-time-center/survey-of-professional-forecasters/historical-data/inflation.xls?la=en"
r = requests.get(url,verify=False)
with open("inflationForecasts.xls", "wb") as code:
    code.write(r.content)

# dls = "http://www.philadelphiafed.org/research-and-data/real-time-center/survey-of-professional-forecasters/historical-data/inflation.xls"
# urllib.urlretrieve(dls, "inflationForecasts.xls")


# In[3]:

# 2. Download and manage data from FRED
gdpDeflatorQ=series('GDPDEF')
gdpDeflatorA=series('A191RD3A086NBEA')
gdpDeflatorQ.apc(method='forward')
gdpDeflatorA.apc(method='forward')
gdpDeflatorQ.window(['07-01-1970','01-01-2200'])
gdpDeflatorA.window(['07-01-1970','01-01-2200'])

interestQ = series('GS1')
interestA = series('GS1')

interestQ.monthtoquarter(method='average')
interestA.monthtoannual(method='average')
interestQ.window(['07-01-1970','01-01-2200'])
interestA.window(['07-01-1970','01-01-2200'])


# In[4]:

# 3. Create forecast series as FRED objects

# 3.1 import the inflation forecasts from Excel file and fill in missing value for 1974:Q3
inflationForecasts = pd.read_excel('inflationForecasts.xls')
inflationForecasts['INFPGDP1YR']=inflationForecasts['INFPGDP1YR'].interpolate()

# 3.2 initialize some FRED objects
gdpDeflatorForecastQ=series('GDPDEF')
gdpDeflatorForecastA=series('GDPDEF')

# 3.3 Associate forecasts with dates. The date should coincide with the start of the period for which the forecast applies.
dates = []
for i,ind in enumerate(inflationForecasts.index):
    year =int(inflationForecasts.iloc[i]['YEAR'])
    quart=int(inflationForecasts.iloc[i]['QUARTER'])
    if quart == 1:
        month = '04'
    elif quart == 2:
        month = '07'
    elif quart == 3:
        month = '10'
    else:
        month = '01'
        year=year+1
    date = month+'-01-'+str(year)
    dates.append(date)
dateNumbers = [dateutil.parser.parse(s) for s in dates]

# 3.4 Create the FRED objects
gdpDeflatorForecastQ.data = inflationForecasts['INFPGDP1YR'].values
gdpDeflatorForecastQ.dates = dates
gdpDeflatorForecastQ.datenumbers = dateNumbers

gdpDeflatorForecastA.data = inflationForecasts['INFPGDP1YR'].values.tolist()
gdpDeflatorForecastA.dates = dates
gdpDeflatorForecastA.datenumbers = dateNumbers
gdpDeflatorForecastA.quartertoannual(method='average')


# In[5]:

# 3.5 Create data frames with forecast inflation, actual inflation, and the 1-year bond rate
window_equalize([gdpDeflatorQ,gdpDeflatorForecastQ,interestQ])
window_equalize([gdpDeflatorA,gdpDeflatorForecastA,interestA])
inflationForecastQDf=pd.DataFrame({'1-year inflation forecast':gdpDeflatorForecastQ.data,'1-year actual inflation':gdpDeflatorQ.data,'1-year nominal interest rate':interestQ.data},index = interestQ.dates)
inflationForecastADf=pd.DataFrame({'1-year inflation forecast':gdpDeflatorForecastA.data,'1-year actual inflation':gdpDeflatorA.data,'1-year nominal interest rate':interestA.data},index = interestA.dates)


# In[6]:

# 3.6 Save data to csv
inflationForecastQDf.to_csv('inflationForecastsQ.csv',index=True,index_label='date')
inflationForecastADf.to_csv('inflationForecastsA.csv',index=True,index_label='date')


# In[7]:

# 4. Plot some things

# 4.1 actual inflation, expected inflation, 1-year interest rate: quarterly
fig=plt.figure()
ax=fig.add_subplot(1,1,1)
ax.plot_date(gdpDeflatorQ.datenumbers,gdpDeflatorQ.data,'b-',lw=3)
ax.plot_date(gdpDeflatorForecastQ.datenumbers,gdpDeflatorForecastQ.data,'r--',lw=3)
ax.plot_date(interestQ.datenumbers,interestQ.data,'m-.',lw=3)
ax.set_title('Quarterly')
ax.set_xlabel('Date')
ax.set_ylabel('%')
ax.legend(['actual $\pi$','forecast $\pi$','interest'],loc='upper right')
# interestQ.recessions()
plt.grid()


# In[8]:

# 4.2 actual inflation, expected inflation, 1-year interest rate: annual
fig=plt.figure()
ax=fig.add_subplot(1,1,1)
ax.plot_date(gdpDeflatorA.datenumbers,gdpDeflatorA.data,'b-o',lw=3)
ax.plot_date(gdpDeflatorForecastA.datenumbers,gdpDeflatorForecastA.data,'r--o',lw=3)
ax.plot_date(interestA.datenumbers,interestA.data,'m-.o',lw=3)
ax.set_title('Annual')
ax.set_xlabel('Date')
ax.set_ylabel('%')
ax.legend(['actual $\pi$','forecast $\pi$','interest'],loc='upper right')
# interestA.recessions()
plt.grid()


# In[9]:

# 5. Real interest rates

# 5.1 Construct real interest rate series: ex ante and ex post
realExAnteA = np.array(interestA.data) - np.array(gdpDeflatorForecastA.data)
realExPostA = np.array(interestA.data) - np.array(gdpDeflatorA.data)
realExAnteQ = np.array(interestQ.data) - np.array(gdpDeflatorForecastQ.data)
realExPostQ = np.array(interestQ.data) - np.array(gdpDeflatorQ.data)


# In[10]:

# 5.2 ex ante and ex post real interest rates: annual
fig=plt.figure()
ax=fig.add_subplot(1,1,1)
ax.plot_date(interestA.datenumbers,realExAnteA,'b-o',lw=3)
ax.plot_date(interestA.datenumbers,realExPostA,'r--o',lw=3)
ax.set_title('Annual real interest rate')
ax.set_xlabel('Date')
ax.set_ylabel('%')
ax.legend(['ex ante','ex post'],loc='upper right')
# interestA.recessions()
plt.grid()


# In[11]:

# 5.2 ex ante and ex post real interest rates: quarterly
fig=plt.figure()
ax=fig.add_subplot(1,1,1)
ax.plot_date(interestQ.datenumbers,realExAnteQ,'b-',lw=3)
ax.plot_date(interestQ.datenumbers,realExPostQ,'r--',lw=3)
ax.set_title('Quarterly real interest rate')
ax.set_xlabel('Date')
ax.set_ylabel('%')
ax.legend(['ex ante','ex post'],loc='upper right')
# interestQ.recessions()
plt.grid()


# In[12]:

# # 6. Consumption Euler equation

# 6.1 create the consumption series
cons=series('PCECA')
defl=series('A191RD3A086NBEA')
window_equalize([cons,defl])

cons.pc(method='backward')
window_equalize([interestA,cons])


# In[13]:

# 6.2 Predicted real interest rate: sigma = 1
sigma = 1
beta = .98
gc=np.mean(cons.data)

rPredA = sigma*np.array(cons.data - np.mean(cons.data)) - 100*np.log(beta)
print(gc)


# In[14]:

# 6.3 Plot the predicted real interest rate
fig=plt.figure()
ax=fig.add_subplot(1,1,1)
ax.plot_date(interestA.datenumbers,realExAnteA,'b-',lw=3)
ax.plot_date(interestA.datenumbers,rPredA,'r--',lw=3)
ax.set_title('Annual ex ante real interest rate')
ax.set_xlabel('Date')
ax.set_ylabel('%')
ax.legend(['actual','predicted'],loc='upper right')
# interestA.recessions()
plt.grid()


# In[15]:

np.corrcoef(cons.data, realExAnteA)


# In[16]:

# 7. Export to notebook to .py
runProcs.exportNb('consumptionEuler')

