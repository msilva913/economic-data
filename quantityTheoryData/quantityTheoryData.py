#!/usr/bin/env python
# coding: utf-8

# In[1]:


import numpy as np
import matplotlib.pyplot as plt
plt.style.use('classic')
import pandas as pd
import quandl as Quandl
import wbdata as wb
from scipy import stats
import runProcs
# get_ipython().run_line_magic('matplotlib', 'inline')


# # Preliminaries
# 
# Import country codes and country lists by income

# In[2]:


# 1. Import country codes and organize

# 1.1 Import country codes and names from the country_codes file from Quandl's WB WDI documentation: https://www.quandl.com/data/WWDI/documentation/documentation
countryCodes = {}

try:
    text_file = open('country_codes', 'r')
    lines = text_file.readlines()
    for line in lines:
        split = line.split('|')
        if len(split)>1:
            if len(split[1])==4:
                countryCodes[split[0]] = split[1][:-1]
except:
    countryCodes = {
 'Afghanistan': 'AFG',
 'Africa': 'AFR',
 'Albania': 'ALB',
 'Algeria': 'DZA',
 'American Samoa': 'ASM',
 'Andorra': 'AND',
 'Angola': 'AGO',
 'Antigua and Barbuda': 'ATG',
 'Arab World': 'ARB',
 'Argentina': 'ARG',
 'Armenia': 'ARM',
 'Aruba': 'ABW',
 'Australia': 'AUS',
 'Austria': 'AUT',
 'Azerbaijan': 'AZE',
 'Bahamas, The': 'BHS',
 'Bahrain': 'BHR',
 'Bangladesh': 'BGD',
 'Barbados': 'BRB',
 'Belarus': 'BLR',
 'Belgium': 'BEL',
 'Belize': 'BLZ',
 'Benin': 'BEN',
 'Bermuda': 'BMU',
 'Bhutan': 'BTN',
 'Bolivia': 'BOL',
 'Bosnia and Herzegovina': 'BIH',
 'Botswana': 'BWA',
 'Brazil': 'BRA',
 'Brunei Darussalam': 'BRN',
 'Bulgaria': 'BGR',
 'Burkina Faso': 'BFA',
 'Burundi': 'BDI',
 'Cabo Verde': 'CPV',
 'Cambodia': 'KHM',
 'Cameroon': 'CMR',
 'Canada': 'CAN',
 'Caribbean small states': 'CSS',
 'Cayman Islands': 'CYM',
 'Central African Republic': 'CAF',
 'Chad': 'TCD',
 'Channel Islands': 'CHI',
 'Chile': 'CHL',
 'China': 'CHN',
 'Colombia': 'COL',
 'Comoros': 'COM',
 'Congo, Dem. Rep.': 'COD',
 'Congo, Rep.': 'COG',
 'Costa Rica': 'CRI',
 "Cote d'Ivoire": 'CIV',
 'Croatia': 'HRV',
 'Cuba': 'CUB',
 'Curacao': 'CUW',
 'Cyprus': 'CYP',
 'Czech Republic': 'CZE',
 'Denmark': 'DNK',
 'Djibouti': 'DJI',
 'Dominica': 'DMA',
 'Dominican Republic': 'DOM',
 'East Asia & Pacific (all income levels)': 'EAS',
 'East Asia & Pacific (developing only)': 'EAP',
 'East Asia and the Pacific (IFC classification)': 'CEA',
 'Ecuador': 'ECU',
 'Egypt, Arab Rep.': 'EGY',
 'El Salvador': 'SLV',
 'Equatorial Guinea': 'GNQ',
 'Eritrea': 'ERI',
 'Estonia': 'EST',
 'Ethiopia': 'ETH',
 'Euro area': 'EMU',
 'Europe & Central Asia (all income levels)': 'ECS',
 'Europe & Central Asia (developing only)': 'ECA',
 'Europe and Central Asia (IFC classification)': 'CEU',
 'European Union': 'EUU',
 'Faeroe Islands': 'FRO',
 'Fiji': 'FJI',
 'Finland': 'FIN',
 'France': 'FRA',
 'French Polynesia': 'PYF',
 'Gabon': 'GAB',
 'Gambia, The': 'GMB',
 'Georgia': 'GEO',
 'Germany': 'DEU',
 'Ghana': 'GHA',
 'Greece': 'GRC',
 'Greenland': 'GRL',
 'Grenada': 'GRD',
 'Guam': 'GUM',
 'Guatemala': 'GTM',
 'Guinea': 'GIN',
 'Guinea-Bissau': 'GNB',
 'Guyana': 'GUY',
 'Haiti': 'HTI',
 'Heavily indebted poor countries (HIPC)': 'HPC',
 'High income': 'HIC',
 'High income: OECD': 'OEC',
 'High income: nonOECD': 'NOC',
 'Honduras': 'HND',
 'Hong Kong SAR, China': 'HKG',
 'Hungary': 'HUN',
 'Iceland': 'ISL',
 'India': 'IND',
 'Indonesia': 'IDN',
 'Iran, Islamic Rep.': 'IRN',
 'Iraq': 'IRQ',
 'Ireland': 'IRL',
 'Isle of Man': 'IMN',
 'Israel': 'ISR',
 'Italy': 'ITA',
 'Jamaica': 'JAM',
 'Japan': 'JPN',
 'Jordan': 'JOR',
 'Kazakhstan': 'KAZ',
 'Kenya': 'KEN',
 'Kiribati': 'KIR',
 'Korea, Dem. Rep.': 'PRK',
 'Korea, Rep.': 'KOR',
 'Kosovo': 'KSV',
 'Kuwait': 'KWT',
 'Kyrgyz Republic': 'KGZ',
 'Lao PDR': 'LAO',
 'Latin America & Caribbean (all income levels)': 'LCN',
 'Latin America & Caribbean (developing only)': 'LAC',
 'Latin America and the Caribbean (IFC classification)': 'CLA',
 'Latvia': 'LVA',
 'Least developed countries: UN classification': 'LDC',
 'Lebanon': 'LBN',
 'Lesotho': 'LSO',
 'Liberia': 'LBR',
 'Libya': 'LBY',
 'Liechtenstein': 'LIE',
 'Lithuania': 'LTU',
 'Low & middle income': 'LMY',
 'Low income': 'LIC',
 'Lower middle income': 'LMC',
 'Luxembourg': 'LUX',
 'Macao SAR, China': 'MAC',
 'Macedonia, FYR': 'MKD',
 'Madagascar': 'MDG',
 'Malawi': 'MWI',
 'Malaysia': 'MYS',
 'Maldives': 'MDV',
 'Mali': 'MLI',
 'Malta': 'MLT',
 'Marshall Islands': 'MHL',
 'Mauritania': 'MRT',
 'Mauritius': 'MUS',
 'Mexico': 'MEX',
 'Micronesia, Fed. Sts.': 'FSM',
 'Middle East & North Africa (all income levels)': 'MEA',
 'Middle East & North Africa (developing only)': 'MNA',
 'Middle East and North Africa (IFC classification)': 'CME',
 'Middle income': 'MIC',
 'Moldova': 'MDA',
 'Monaco': 'MCO',
 'Mongolia': 'MNG',
 'Montenegro': 'MNE',
 'Morocco': 'MAR',
 'Mozambique': 'MOZ',
 'Myanmar': 'MMR',
 'Namibia': 'NAM',
 'Nepal': 'NPL',
 'Netherlands': 'NLD',
 'New Caledonia': 'NCL',
 'New Zealand': 'NZL',
 'Nicaragua': 'NIC',
 'Niger': 'NER',
 'Nigeria': 'NGA',
 'North Africa': 'NAF',
 'North America': 'NAC',
 'Northern Mariana Islands': 'MNP',
 'Norway': 'NOR',
 'OECD members': 'OED',
 'Oman': 'OMN',
 'Other small states': 'OSS',
 'Pacific island small states': 'PSS',
 'Pakistan': 'PAK',
 'Palau': 'PLW',
 'Panama': 'PAN',
 'Papua New Guinea': 'PNG',
 'Paraguay': 'PRY',
 'Peru': 'PER',
 'Philippines': 'PHL',
 'Poland': 'POL',
 'Portugal': 'PRT',
 'Puerto Rico': 'PRI',
 'Qatar': 'QAT',
 'Romania': 'ROU',
 'Russian Federation': 'RUS',
 'Rwanda': 'RWA',
 'Samoa': 'WSM',
 'San Marino': 'SMR',
 'Sao Tome and Principe': 'STP',
 'Saudi Arabia': 'SAU',
 'Senegal': 'SEN',
 'Serbia': 'SRB',
 'Seychelles': 'SYC',
 'Sierra Leone': 'SLE',
 'Singapore': 'SGP',
 'Sint Maarten (Dutch part)': 'SXM',
 'Slovak Republic': 'SVK',
 'Slovenia': 'SVN',
 'Small states': 'SST',
 'Solomon Islands': 'SLB',
 'Somalia': 'SOM',
 'South Africa': 'ZAF',
 'South Asia': 'SAS',
 'South Asia (IFC classification)': 'CSA',
 'South Sudan': 'SSD',
 'Spain': 'ESP',
 'Sri Lanka': 'LKA',
 'St. Kitts and Nevis': 'KNA',
 'St. Lucia': 'LCA',
 'St. Martin (French part)': 'MAF',
 'St. Vincent and the Grenadines': 'VCT',
 'Sub-Saharan Africa (IFC classification)': 'CAA',
 'Sub-Saharan Africa (all income levels)': 'SSF',
 'Sub-Saharan Africa (developing only)': 'SSA',
 'Sub-Saharan Africa excluding South Africa': 'SXZ',
 'Sub-Saharan Africa excluding South Africa and Nigeria': 'XZN',
 'Sudan': 'SDN',
 'Suriname': 'SUR',
 'Swaziland': 'SWZ',
 'Sweden': 'SWE',
 'Switzerland': 'CHE',
 'Syrian Arab Republic': 'SYR',
 'Tajikistan': 'TJK',
 'Tanzania': 'TZA',
 'Thailand': 'THA',
 'Timor-Leste': 'TLS',
 'Togo': 'TGO',
 'Tonga': 'TON',
 'Trinidad and Tobago': 'TTO',
 'Tunisia': 'TUN',
 'Turkey': 'TUR',
 'Turkmenistan': 'TKM',
 'Turks and Caicos Islands': 'TCA',
 'Tuvalu': 'TUV',
 'Uganda': 'UGA',
 'Ukraine': 'UKR',
 'United Arab Emirates': 'ARE',
 'United Kingdom': 'GBR',
 'United States': 'USA',
 'Upper middle income': 'UMC',
 'Uruguay': 'URY',
 'Uzbekistan': 'UZB',
 'Vanuatu': 'VUT',
 'Venezuela, RB': 'VEN',
 'Vietnam': 'VNM',
 'Virgin Islands (U.S.)': 'VIR',
 'West Bank and Gaza': 'PSE',
 'World': 'WLD',
 'Yemen, Rep.': 'YEM',
 'Zambia': 'ZMB',
 'Zimbabwe': 'ZWE'}
    
        
#1.2 Use wbdata to get lists of country codes by income groups
countriesIncomeAll =  [i['id'] for i in wb.get_country(incomelevel=['LIC','MIC','HIC'],display=False)]
countriesIncomeH = [i['id'] for i in wb.get_country(incomelevel=['HIC'],display=False)]
countriesIncomeM = [i['id'] for i in wb.get_country(incomelevel=['MIC'],display=False)]
countriesIncomeL = [i['id'] for i in wb.get_country(incomelevel=['LIC'],display=False)]

countriesIncomeOecd = ['AUS','CAN','CHL','CZE','DNK','EST','HUN','ISL','ISR','JPN'
                       ,'KOR','NZL','NOR''POL','SVK','SVN','SWE','CHE','USA']


# # Import data from Quandl

# In[ ]:


# 2. Import data from Quandl

# 2.1 Money supply (LCU)
moneyDf = pd.DataFrame({})

for name,key in countryCodes.items():
    try:
        df = Quandl.get('WWDI/'+key+'_FM_LBL_MONY_CN',authtoken="QqLL1AFCjc31_MVo4qsU")
        df.columns = [key]
        moneyDf = pd.concat([moneyDf,df],axis=1)
    except:
        pass

# 2.2 GDP deflator
deflatorDf = pd.DataFrame({})

for name,key in countryCodes.items():
    try:
        df = Quandl.get('WWDI/'+key+'_NY_GDP_DEFL_ZS',authtoken="QqLL1AFCjc31_MVo4qsU")
        df.columns = [key]
        deflatorDf = pd.concat([deflatorDf,df],axis=1)
    except:
        pass

# 2.3 Real GDP
gdpDf = pd.DataFrame({})

for name,key in countryCodes.items():
    try:
        df = Quandl.get('WWDI/'+key+'_NY_GDP_MKTP_KD',authtoken="QqLL1AFCjc31_MVo4qsU")
        df.columns = [key]
        gdpDf = pd.concat([gdpDf,df],axis=1)
    except:
        pass

# 2.4 Exahange rate relative to USD
exchangeDf = pd.DataFrame({})

for name,key in countryCodes.items():
    try:
        df = Quandl.get('WWDI/'+key+'_PA_NUS_FCRF',authtoken="QqLL1AFCjc31_MVo4qsU")
        df.columns = [key]
        exchangeDf = pd.concat([exchangeDf,df],axis=1)
    except:
        pass

# 2.5 Nominal interest rate (lending rate)
interestDf = pd.DataFrame({})

for name,key in countryCodes.items():
    try:
        df = Quandl.get('WWDI/'+key+'_FR_INR_LEND',authtoken="QqLL1AFCjc31_MVo4qsU")
        df.columns = [key]
        interestDf = pd.concat([interestDf,df],axis=1)
    except:
        pass


# # Create data sets: money, prices, and output

# In[ ]:


# 3. Create datasets for quantity theory without interest and exchange rates

# 3.1 Dataframes to use
dataFrames = [moneyDf, deflatorDf, gdpDf]

# 3.2 Identify the codes for countries with at least 10 years of consecutive data for each series
availableCodes = []
for code in countryCodes.values():
    if all(code in frame for frame in dataFrames):
        if any( all(np.isnan(x) for x in frame[code]) for frame in dataFrames):
            print(code)
        else:
            availableCodes.append(code)        
            
print('Number of countries: ',len(availableCodes))

# 3.3 Construct the dataset including the average growth rates of variabes for each country
includedCodes = []
obs = []
mData = []
pData = []
yData = []
    
for c in availableCodes:
    count = 0
    ind = []
    
    for i in dataFrames[0].index[1:]:

        noneNan = all( not np.isnan(frame[c].loc[i]) for frame in dataFrames)
        anyNan = any( np.isnan(frame[c].loc[i]) for frame in dataFrames)

        if noneNan:
            count+=1
            ind.append(i)
        elif anyNan and count>0:
            break

    if count >9:
        m = (moneyDf[c].loc[ind[-1]]/moneyDf[c].loc[ind[0]])**(1/count)-1
        p = (deflatorDf[c].loc[ind[-1]]/deflatorDf[c].loc[ind[0]])**(1/count)-1
        y = (gdpDf[c].loc[ind[-1]]/gdpDf[c].loc[ind[0]])**(1/count)-1

        includedCodes.append(c)
        mData.append(np.around(m,5))
        pData.append(np.around(p,5))
        yData.append(np.around(y,5))
        obs.append(count)


# 3.3 Identify the names of the countries that are incuded
includedNames = []
for c in includedCodes:
    for name, code in countryCodes.items():
        if c == code:
            includedNames.append(name)

# 3.4 Create the main dataframe
qtyTheoryData = pd.DataFrame({'iso code':includedCodes,'observations':obs,'inflation':pData,'money growth':mData,'gdp growth':yData},index = includedNames)
qtyTheoryData = qtyTheoryData[['iso code','observations','inflation','money growth','gdp growth']]
qtyTheoryData = qtyTheoryData.sort_index()

# 3.5 Create dataframes organized by income levels
indexL=[]
indexM=[]
indexH=[]
indexOecd=[]

for country in qtyTheoryData.index:
    code = qtyTheoryData['iso code'].loc[country]
    if code in countriesIncomeL:
        indexL.append(country)
    if code in countriesIncomeM:
        indexM.append(country)
    if code in countriesIncomeH:
        indexH.append(country)
    if code in countriesIncomeOecd:
        indexOecd.append(country)

# Drop countries with inf values
qtyTheoryData = qtyTheoryData.replace([np.inf, -np.inf], np.nan).dropna()

qtyTheoryDataL = qtyTheoryData.loc[indexL]
qtyTheoryDataM = qtyTheoryData.loc[indexM]
qtyTheoryDataH = qtyTheoryData.loc[indexH]
qtyTheoryDataOecd = qtyTheoryData.loc[indexOecd]

# 3.6 Export dataframes to csv
qtyTheoryData.to_csv('qtyTheoryData.csv',index=True,index_label='country')
qtyTheoryDataL.to_csv('qtyTheoryDataL.csv',index=True,index_label='country')
qtyTheoryDataM.to_csv('qtyTheoryDataM.csv',index=True,index_label='country')
qtyTheoryDataH.to_csv('qtyTheoryDataH.csv',index=True,index_label='country')
qtyTheoryDataOecd.to_csv('qtyTheoryDataOecd.csv',index=True,index_label='country')


# # Create data sets: money, prices, output, interest, and exchange rates

# In[ ]:


# 4. Create datasets for quantity theory with interest and exchange rates

# 4.1 Dataframes to use
dataFrames = [moneyDf, deflatorDf, gdpDf,interestDf,exchangeDf]

# 4.2 Identify the codes for countries with at leaset 10 years of consecutive data for each series
availableCodes = []
for code in countryCodes.values():
    if all(code in frame for frame in dataFrames):
        if any( all(np.isnan(x) for x in frame[code]) for frame in dataFrames):
            print(code)
        else:
            availableCodes.append(code)        
            
print('Number of countries: ',len(availableCodes))

# 4.3 Construct the dataset including the average growth rates of variabes for each country
includedCodes = []
obs = []
mData = []
pData = []
yData = []
iData = []
eData = []
    
for c in availableCodes:
    count = 0
    ind = []
    
    for i in dataFrames[0].index[1:]:

        noneNan = all( not np.isnan(frame[c].loc[i]) for frame in dataFrames)
        anyNan = any( np.isnan(frame[c].loc[i]) for frame in dataFrames)

        if noneNan:
            count+=1
            ind.append(i)
        elif anyNan and count>0:
            break

    if count >9:
        m = (moneyDf[c].loc[ind[-1]]/moneyDf[c].loc[ind[0]])**(1/count)-1
        p = (deflatorDf[c].loc[ind[-1]]/deflatorDf[c].loc[ind[0]])**(1/count)-1
        y = (gdpDf[c].loc[ind[-1]]/gdpDf[c].loc[ind[0]])**(1/count)-1
        e = (exchangeDf[c].loc[ind[-1]]/exchangeDf[c].loc[ind[0]])**(1/count)-1
        rate = np.mean(interestDf[c].iloc[1:])/100

        includedCodes.append(c)
        mData.append(np.around(m,5))
        pData.append(np.around(p,5))
        yData.append(np.around(y,5))
        eData.append(np.around(e,5))
        iData.append(np.around(rate,5))
        obs.append(count)


# 4.3 Identify the names of the countries that are incuded
includedNames = []
for c in includedCodes:
    for name, code in countryCodes.items():
        if c == code:
            includedNames.append(name)

# 4.4 Create the main dataframe
qtyTheoryData = pd.DataFrame({'iso code':includedCodes,'observations':obs,'inflation':pData,'money growth':mData,'gdp growth':yData,'nominal interest rate':iData,'exchange rate depreciation':eData},index = includedNames)
qtyTheoryData = qtyTheoryData[['iso code','observations','inflation','money growth','gdp growth','nominal interest rate','exchange rate depreciation']]
qtyTheoryData = qtyTheoryData.sort_index()

# 4.5 Create dataframes organized by income levels
indexL=[]
indexM=[]
indexH=[]
indexOecd=[]

for country in qtyTheoryData.index:
    code = qtyTheoryData['iso code'].loc[country]
    if code in countriesIncomeL:
        indexL.append(country)
    if code in countriesIncomeM:
        indexM.append(country)
    if code in countriesIncomeH:
        indexH.append(country)
    if code in countriesIncomeOecd:
        indexOecd.append(country)
        
# Drop countries with inf values
qtyTheoryData = qtyTheoryData.replace([np.inf, -np.inf], np.nan).dropna()
        
qtyTheoryDataL = qtyTheoryData.loc[indexL]
qtyTheoryDataM = qtyTheoryData.loc[indexM]
qtyTheoryDataH = qtyTheoryData.loc[indexH]
qtyTheoryDataOecd = qtyTheoryData.loc[indexOecd]

# 4.6 Export dataframes to csv
qtyTheoryData.to_csv('qtyTheoryOpenData.csv',index=True,index_label='country')
qtyTheoryDataL.to_csv('qtyTheoryOpenDataL.csv',index=True,index_label='country')
qtyTheoryDataM.to_csv('qtyTheoryOpenDataM.csv',index=True,index_label='country')
qtyTheoryDataH.to_csv('qtyTheoryOpenDataH.csv',index=True,index_label='country')
qtyTheoryDataOecd.to_csv('qtyTheoryOpenDataOecd.csv',index=True,index_label='country')


# In[ ]:


# 5. Export notebook to python script
runProcs.exportNb('quantityTheoryData')

