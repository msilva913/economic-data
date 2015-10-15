from __future__ import division
import numpy as np
import pandas as pd
import wbdata

def create(dataFrame,indicators,isoCodes,levels=None,csvFilename=None,decimals = 5):
    
    indicatorNames = []
    for n,elem in enumerate(indicators):
        indicatorNames.append(indicators[elem])
    
    indicatorNames = sorted(indicatorNames)

    dropped=[]
    include=[]

    dataArray = np.ndarray(shape=(0,len(indicators)))
    
    obs=[]
    codes=[]

    for country, newDf in dataFrame.groupby(level=0):

        dataArrayTemp = np.ndarray(shape=(0,len(indicators)))
        count=0

        # Check if an entire series is missing
        if any(all(np.isnan(x) for x in newDf[l]) for l in indicatorNames):
            print('At least one series missing for '+str(country))
            dropped.append(str(country))

        else:
            for index, row in newDf.sort(ascending=False).iterrows():
                if all(~np.isnan(row[l]) for l in indicatorNames):
                    dataArrayTemp = np.vstack([dataArrayTemp,row])
                    count+=1
                elif any(np.isnan(row[l]) for l in indicatorNames) and count>0:
                    break
        if count>=10:
            newRow = []
            for c,column in enumerate(dataArrayTemp.T):
                if indicatorNames[c] in levels:
                    newRow.append(np.around(np.mean(column),5))
                else:
                    newRow.append(np.around(np.power(column[0]/column[-1],1/(count-1))-1,5))
            dataArray = np.vstack([dataArray,newRow])
            obs.append(count)
            include.append(str(country))
            codes.append(isoCodes.loc[country][0])
        else:
            dropped.append(str(country))

    d = {'iso code': codes,
         'observations': np.around(obs,decimals)}
    
    for n,elem in enumerate(indicatorNames):
        d[elem] = dataArray.T[n]

    qtyTheoryData = pd.DataFrame(d, index=include)
    colNames = ['iso code','observations']+indicatorNames
    qtyTheoryData = qtyTheoryData[colNames]
    if 'interest rate' in colNames:
        qtyTheoryData['interest rate'] = qtyTheoryData['interest rate']/100
    
    if type(csvFilename)==str:
        
        if csvFilename[-4:]!='.csv':
            csvFilename=csvFilename+'.csv'
        qtyTheoryData.to_csv(csvFilename,index=True,index_label='country')
            
    return qtyTheoryData, include, dropped