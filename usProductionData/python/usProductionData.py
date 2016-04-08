
# coding: utf-8

# In[1]:

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as dts
from fredpy import series, window_equalize
import pandas as pd
import runProcs
# get_ipython().magic('matplotlib inline')


# In[2]:

# 0. Setup: Formatting commands and definitions.

# 0.1 general plot settings

# Make all plotted axis lables and tick lables bold 15 pt font
font = {'weight' : 'bold',
        'size'   : 15}
axes={'labelweight' : 'bold'}
plt.rc('font', **font)
plt.rc('axes', **axes)

# Add some space around the tick lables for better readability
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
majorLocator_shares = plt.MultipleLocator(0.2)


# In[ ]:

# 1. Setup for the construction of K and A

# 1.1 Parameters for the model

delta0= 0.06
g0    = 0.03
alpha = 0.35

# 1.2 Some options for the program:
# 
#    If output_solow == TRUE, then Y = C + I.                   Else: Y = C + I + G + NX (default)
#    If calibrate_delta == 'TRUE', then calibrate.              Else: delta=delta0 (default)
#    If calibrate_g == 'TRUE', then calibrate. (default)        Else: g = g0 
#    If growth_I == 'TRUE', then use g(I) for calbrating delta. Else: use G(Y) (default)
# 

output_solow = False
calibrate_delta = False
calibrate_g = True
growth_I = False


# 1.3 Define the function for computing the capital series

def capitalSeries(i,k0,delta):
    t0 = len(i)-1
    k = [k0]
    for t in range(t0):
        k.append(i[t]+(1-delta)*k[t])

    return np.array(k)


# In[ ]:

# 2. Import and manage data from FRED

# 2.1 Annual data
investmentA = series('GPDIA')
consumptionA = series('PCECA')
governmentA = series('GCEA')
exportsA = series('EXPGSA')
importsA = series('IMPGSA')
netExportsA = series('A019RC1A027NBEA')
deflatorA = series('A191RD3A086NBEA')
depreciationA = series('Y0000C1A027NBEA')
gdpA = series('GDPA')
tfpA = series('GDPA')
capitalA = series('GDPA')
laborA = series('B4701C0A222NBEA')# BEA index: fred('HOANBS') / .quartertoannual(method='AVG')

annualSeries = [investmentA,consumptionA,governmentA,exportsA,importsA,netExportsA,deflatorA,depreciationA,gdpA,tfpA,capitalA,laborA]
window_equalize([investmentA,consumptionA,governmentA,netExportsA,exportsA,importsA,deflatorA,depreciationA,gdpA,tfpA,capitalA,laborA])

# 2.2 Compute real annual data series
investmentA.data= 100*investmentA.data/deflatorA.data
consumptionA.data = 100*consumptionA.data/deflatorA.data
governmentA.data = 100*governmentA.data/deflatorA.data
exportsA.data = 100*exportsA.data/deflatorA.data
importsA.data = 100*importsA.data/deflatorA.data
netExportsA.data = 100*netExportsA.data/deflatorA.data
gdpA.data= 100*gdpA.data/deflatorA.data
TA     = len(investmentA.data)

# 2.3 Quarterly data
investmentQ  = series('GPDI')
investmentQ4  = series('GPDI')
consumptionQ  = series('PCEC')
governmentQ = series('GCE')
exportsQ = series('EXPGS')
importsQ = series('IMPGS')
netExportsQ = series('NETEXP')
deflatorQ  = series('GDPDEF')
gdpQ  = series('GDP')
tfpQ  = series('GDP')
capitalQ  = series('GDP')
laborQ    = series('HOANBS') # L    = fred('B4701C0A222NBEA')

quarterlySeries = [investmentQ,consumptionQ,governmentQ,exportsQ,importsQ,netExportsQ,deflatorQ,gdpQ,tfpQ,capitalQ,laborQ]
window_equalize([investmentQ,consumptionQ,governmentQ,netExportsQ,exportsQ,importsQ,deflatorQ,gdpQ,tfpQ,capitalQ,laborQ])

# 2.2 Compute real annual data series
investmentQ.data= 100*investmentQ.data/deflatorQ.data
investmentQ4.data= 100*investmentQ4.data/deflatorQ.data
consumptionQ.data = 100*consumptionQ.data/deflatorQ.data
governmentQ.data = 100*governmentQ.data/deflatorQ.data
netExportsQ.data = 100*netExportsQ.data/deflatorQ.data
exportsQ.data = 100*exportsQ.data/deflatorQ.data
importsQ.data = 100*importsQ.data/deflatorQ.data
gdpQ.data= 100*gdpQ.data/deflatorQ.data
TQ     = len(investmentQ.data)

# 2.4 Compute real annual data series. Note that investment is at a quarterly rate
# investmentQ4= [a/4 for a in investmentQ.data]
# realGdpQ= [100*a/b for a,b in zip(gdpQ.data,deflatorQ.data)]

# 2.5 Find the base year for the deflator:
baseYear = deflatorA.units[6:10]
laborBaseYear= laborQ.units[6:10]


# In[ ]:

# 3. Parameter calibration using the annual series

# 3.1 Use Y = C + I as the measure for output if that was requested above
if output_solow == True:
    y0A= consumptionA.data+investmentA.data
    gdpA.data = y0A
    y0Q = consumptionQ.data+investmentQ.data
    gdpQ.data = y0Q

# 3.2 form the ratios of depreciation and investment to output
depreciationYRatio= np.mean([d/y for d,y in zip(depreciationA.data,gdpA.data)])
iYRatio = np.mean([i/y for i,y in zip(investmentA.data,gdpA.data)])


# 3.3 compute the annual growth rates of output and investment
growthY = (gdpA.data[-1]/gdpA.data[0])**(1/TA)-1
growthI = (investmentA.data[-1]/investmentA.data[0])**(1/TA)-1

# 3.4 Use the either the growth rate of Y or I to calibrate g if specified above
if calibrate_g == True:
    if growth_I == True:
        g = growthI
    else:
        g = growthY
else:
    g = g0

    
# 3.5 use the ratios of depreciation and investment to output to calibrate delta if requested
if calibrate_delta == True:
    delta = depreciationYRatio*g/(iYRatio-depreciationYRatio)
else:
    delta = delta0

# 3.6 print the computed rates for inspection
print('gI:'   ,growthI)
print('gY:'   ,growthY)
print('delta:',delta)
print('s:', iYRatio)


# In[ ]:

# 4. Implement the perpetual inventory method

# 4.1 Annual capital series
k0A = investmentA.data[0]/(delta + g)
capitalA.data = capitalSeries(investmentA.data,k0A,delta)

# 4.2 Quarterly capital series
k0Q = investmentQ4.data[0]/(delta/4 + g/4)
capitalQ.data = capitalSeries(investmentQ4.data,k0Q,delta/4)


# In[ ]:

# 5. Plot the capital series. Note that the annual and quarterly series should and do align approximately.

fig = plt.figure()
ax = fig.add_subplot(1,1,1)
ax.plot_date(capitalA.datenumbers,capitalA.data/1000,'b-',lw = 3)
ax.plot_date(capitalQ.datenumbers,capitalQ.data/1000,'r-',lw = 3)
ax.xaxis.set_major_locator(years10)
ax.set_ylabel('Trillions of \n '+baseYear+' $')
capitalA.recessions()
fig.autofmt_xdate()
plt.title('Capital Stock')
ax.legend(['Annual','Quarterly'],loc='upper left')
ax.grid(True)
# plt.savefig('fig_US_Production_Capital_QA.png',bbox_inches='tight')

fig = plt.figure()
ax = fig.add_subplot(1,1,1)
ax.plot_date(capitalA.datenumbers,capitalA.data/1000,'b-',lw = 3)
ax.xaxis.set_major_locator(years10)
ax.set_ylabel('Trillions of \n '+baseYear+' $')
capitalA.recessions()
fig.autofmt_xdate()
plt.title('Capital Stock: Annual')
ax.grid(True)
# plt.savefig('fig_US_Production_Capital_A.png',bbox_inches='tight')

fig = plt.figure()
ax = fig.add_subplot(1,1,1)
ax.plot_date(capitalQ.datenumbers,capitalQ.data/1000,'b-',lw = 3)
ax.xaxis.set_major_locator(years10)
ax.set_ylabel('Trillions of \n '+baseYear+' $')
capitalA.recessions()
fig.autofmt_xdate()
plt.title('Capital Stock: Quarterly')
ax.grid(True)
# plt.savefig('../img/fig_US_Production_Capital_A.png',bbox_inches='tight')


# In[ ]:

# 6. Save data to csv files

# 6.1 Annual data

YearA       = [a[0:4]     for a in capitalA.dates]
OutputA     = [round(x,1) for x in gdpA.data]
ConsumptionA= [round(x,1) for x in consumptionA.data]
InvestmentA = [round(x,1) for x in investmentA.data]
GovernmentA = [round(x,1) for x in governmentA.data]
ImportsA = [round(x,1) for x in netExportsA.data]
ExportsA = [round(x,1) for x in netExportsA.data]
NetExportsA = [round(x,1) for x in netExportsA.data]
CapitalA    = [round(x,1) for x in capitalA.data]
LaborA      = [round(x,1) for x in laborA.data]

columnsA = ['Year','Output [Bil. of '+baseYear+' Dollars]','Consumption [Bil. of '+baseYear+' Dollars]','Investment [Bil. of '+baseYear+' Dollars]','Government Purchases [Bil. of '+baseYear+' Dollars]','Exports [Bil. of '+baseYear+' Dollars]','Imports [Bil. of '+baseYear+' Dollars]','Net Exports [Bil. of '+baseYear+' Dollars]','Capital [Bil. of '+baseYear+' Dollars]','Labor [Mil. of Hours]']

df = pd.DataFrame({
    'Year':YearA,
    'Output [Bil. of '+baseYear+' Dollars]':OutputA,
    'Consumption [Bil. of '+baseYear+' Dollars]':ConsumptionA,
    'Investment [Bil. of '+baseYear+' Dollars]':InvestmentA,
    'Government Purchases [Bil. of '+baseYear+' Dollars]':GovernmentA,
    'Exports [Bil. of '+baseYear+' Dollars]':ExportsA,
    'Imports [Bil. of '+baseYear+' Dollars]':ImportsA,
    'Net Exports [Bil. of '+baseYear+' Dollars]':NetExportsA,
    'Capital [Bil. of '+baseYear+' Dollars]':CapitalA,
    'Labor [Mil. of Hours]':LaborA})
df = df[columnsA]
df.to_csv('../csv/US_Production_A_Data.csv',index=False)

# 6.2 Quarterly data

DateQ     = [a     for a in capitalQ.dates]
OutputQ   = [round(x,1) for x in gdpQ.data]
ConsumptionQ= [round(x,1) for x in consumptionQ.data]
InvestmentQ = [round(x,1) for x in investmentQ.data]
GovernmentQ = [round(x,1) for x in governmentQ.data]
ImportsQ = [round(x,1) for x in importsQ.data]
ExportsQ = [round(x,1) for x in exportsQ.data]
NetExportsQ = [round(x,1) for x in netExportsQ.data]
CapitalQ  = [round(x,1) for x in capitalQ.data]
LaborQ    = [round(x,1) for x in laborQ.data]


columnsQ = ['Date','Output [Bil. of '+baseYear+' Dollars]','Consumption [Bil. of '+baseYear+' Dollars]','Investment [Bil. of '+baseYear+' Dollars]','Government Purchases [Bil. of '+baseYear+' Dollars]','Exports [Bil. of '+baseYear+' Dollars]','Imports [Bil. of '+baseYear+' Dollars]','Net Exports [Bil. of '+baseYear+' Dollars]','Capital [Bil. of '+baseYear+' Dollars]','Labor [Index: '+laborBaseYear+'=100]']
df = pd.DataFrame({
    'Date':DateQ,
    'Output [Bil. of '+baseYear+' Dollars]':OutputQ,
    'Consumption [Bil. of '+baseYear+' Dollars]':ConsumptionQ,
    'Investment [Bil. of '+baseYear+' Dollars]':InvestmentQ,
    'Government Purchases [Bil. of '+baseYear+' Dollars]':GovernmentQ,
    'Exports [Bil. of '+baseYear+' Dollars]':ExportsQ,
    'Imports [Bil. of '+baseYear+' Dollars]':ImportsQ,
    'Net Exports [Bil. of '+baseYear+' Dollars]':NetExportsQ,
    'Capital [Bil. of '+baseYear+' Dollars]':CapitalQ,
    'Labor [Index: '+laborBaseYear+'=100]':LaborQ})
df = df[columnsQ]
df.to_csv('../csv/US_Production_Q_Data.csv',index=False)


# In[ ]:

# 7. Compute the Solow residuals: 

# 7.1 Annual residual
capitalA.apc()
tfpA.apc()
laborA.apc()
gdpA.apc()
consumptionA.apc()
investmentA.apc()
governmentA.apc()
exportsA.apc()
importsA.apc()
netExportsA.apc()

gYA = gdpA.data
gLA = laborA.data
gKA = capitalA.data

tfpA.data = gYA - alpha*gKA - (1-alpha)*gLA

# 7.2. Compute the Solow residual: Quarterly

capitalQ.apc()
tfpQ.apc()
laborQ.apc()
gdpQ.apc()
consumptionQ.apc()
investmentQ.apc()
governmentQ.apc()
exportsQ.apc()
importsQ.apc()

netExportsQ.data = np.array(netExportsQ.data)
netExportsQ.apc()

gYQ = gdpQ.data
gLQ = laborQ.data
gKQ = capitalQ.data

tfpQ.data = gYQ - alpha*gKQ - (1-alpha)*gLQ


# In[ ]:

# 11. Construct some plots

fig = plt.figure() 
ax = fig.add_subplot(1,1,1)
ax.plot_date(gdpA.datenumbers,gdpA.data,'b-',lw = 3)
ax.plot_date(tfpA.datenumbers,tfpA.data,'g-',lw = 3)
ax.xaxis.set_major_locator(years10)
ax.set_ylabel('%')
gdpA.recessions()
fig.autofmt_xdate()
ax.grid(True)
ax.legend(['GDP growth','Solow Residual'],bbox_to_anchor=(0., 1.02, 1., .102), loc=3,
       ncol=3, mode="expand", borderaxespad=0.,fontsize=15)
# plt.savefig('fig_US_Production_ya_growth_A.png',bbox_inches='tight')

# 11.2 Figure for website: Annual growth in Y, L, K, and A
fig = plt.figure(figsize=(10, 6)) 
ax = fig.add_subplot(2,2,1)
ax.plot_date(tfpA.datenumbers,tfpA.data,'b-',lw = 3,alpha = 0.75)
ax.set_title('TFP Growth')
ax.xaxis.set_major_locator(years10)
ax.set_ylabel('%')
tfpA.recessions()
fig.autofmt_xdate()
ax.locator_params(axis='y',nbins=6)
ax.grid(True)

ax = fig.add_subplot(2,2,2)
ax.plot_date(gdpA.datenumbers,gdpA.data,'b-',lw = 3,alpha = 0.75)
ax.set_title('Real GDP Growth')
ax.xaxis.set_major_locator(years10)
ax.locator_params(axis='y',nbins=6)
gdpA.recessions()
fig.autofmt_xdate()
ax.grid(True)

ax = fig.add_subplot(2,2,3)
ax.plot_date(laborA.datenumbers,laborA.data,'b-',lw = 3,alpha = 0.75)
ax.xaxis.set_major_locator(years10)
laborA.recessions()
ax.set_ylabel('%')
ax.set_title('Labor Growth')
ax.locator_params(axis='y',nbins=6)
fig.autofmt_xdate()
ax.grid(True)

ax = fig.add_subplot(2,2,4)
ax.plot_date(capitalA.datenumbers,capitalA.data,'b-',lw = 3,alpha = 0.75)
ax.xaxis.set_major_locator(years10)
ax.set_title('Capital Growth')
ax.locator_params(axis='y',nbins=6)
capitalA.recessions()
fig.autofmt_xdate()
ax.grid(True)

plt.savefig('../img/fig_US_Production_A_site.png',bbox_inches='tight')


# 11.3 Quarterly GDP growth and the SOlow residual
fig = plt.figure() 
ax = fig.add_subplot(1,1,1)
ax.plot_date(gdpQ.datenumbers,gdpQ.data,'b-',lw = 3)
ax.plot_date(tfpQ.datenumbers,tfpQ.data,'g-',lw = 3)
ax.xaxis.set_major_locator(years10)
ax.set_ylabel('%')
gdpQ.recessions()
fig.autofmt_xdate()
ax.grid(True)
ax.legend(['GDP growth','Solow Residual'],bbox_to_anchor=(0., 1.02, 1., .102), loc=3,
       ncol=3, mode="expand", borderaxespad=0.,fontsize=15)
# plt.savefig('../img/fig_US_Production_ya_growth_Q.png',bbox_inches='tight')


# In[ ]:

# 10. Save growth rate data to csv files

# 10.1 Annual data

YearA     = [a[0:4]     for a in tfpA.dates]
CapitalA  = [round(x,1) for x in capitalA.data]
LaborA    = [round(x,1) for x in laborA.data]
OutputA   = [round(x,1) for x in gdpA.data]
ConsumptionA   = [round(x,1) for x in consumptionA.data]
InvestmentA   = [round(x,1) for x in investmentA.data]
GovernmentA   = [round(x,1) for x in governmentA.data]
ExportsA   = [round(x,1) for x in exportsA.data]
ImportsA   = [round(x,1) for x in importsA.data]
NetExportsA   = [round(x,1) for x in netExportsA.data]


columnsA = ['Year','Output Growth','Consumption Growth','Investment Growth','Government Purchases Growth','Exports Growth','Imports Growth','Net Exports Growth','Capital Growth','Labor Growth']
data = [YearA,OutputA,ConsumptionA,InvestmentA,GovernmentA,ExportsA,ImportsA,NetExportsA,CapitalA,LaborA]
dA ={}
for n,c in enumerate(columnsA):
    dA[columnsA[n]]=data[n]

df = pd.DataFrame(dA)
df = df[columnsA]
df.to_csv('../csv/US_Production_A_Data_Growth_Rates.csv',index=False)


# 10.2 Quarterly data

DateQ     = [a     for a in tfpQ.dates]
CapitalQ  = [round(x,1) for x in capitalQ.data]
LaborQ    = [round(x,1) for x in laborQ.data]
OutputQ   = [round(x,1) for x in gdpQ.data]
ConsumptionQ   = [round(x,1) for x in consumptionQ.data]
InvestmentQ   = [round(x,1) for x in investmentQ.data]
GovernmentQ   = [round(x,1) for x in governmentQ.data]
ExportsQ   = [round(x,1) for x in exportsQ.data]
ImportsQ   = [round(x,1) for x in importsQ.data]
NetExportsQ   = [round(x,1) for x in netExportsQ.data]

columnsQ = ['Year','Output Growth','Consumption Growth','Investment Growth','Government Purchases Growth','Exports Growth','Imports Growth','Net Exports Growth','Capital Growth','Labor Growth']
data = [DateQ,OutputQ,ConsumptionQ,InvestmentQ,GovernmentQ,ExportsQ,ImportsQ,NetExportsQ,CapitalQ,LaborQ]
dQ ={}
for n,c in enumerate(columnsQ):
    dQ[columnsQ[n]]=data[n]

df = pd.DataFrame(dQ)
df = df[columnsQ]
df.to_csv('../csv/US_Production_Q_Data_Growth_Rates.csv',index=False)


# In[ ]:

# 11. Export notebook to python script
progName = 'usProductionData'
runProcs.exportNb(progName)

