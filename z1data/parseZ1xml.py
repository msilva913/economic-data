from lxml import etree
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import datetime


def createLegend(root):

    legend_df = pd.DataFrame(columns=['Series Name','Description','Frequency','Start','End'])
    x = 0

    for levelA in root:
        for levelB in levelA[4:-1]:
            entry = []
            ident = levelB.get('SERIES_NAME')
            freq = ident[-1]
            entry.append(ident)
            for levelC in levelB:
                for n,levelD in enumerate(levelC):
                    if n == 0:
                        entry.append(levelD[1].text)
                        entry.append(freq)                
            for levelC in [levelB[1],levelB[-1]]:
                d= levelC.get('TIME_PERIOD')
                d= datetime.datetime.strptime(d, '%Y-%m-%d').strftime('%m-%d-%Y')
                entry.append(d)

            legend_df.loc[x] = entry
            x+=1
            
    legend_df.to_csv('z1Legend.csv')

    return legend_df

def getSeries(name):
    
    dates = []
    value= np.array([])
    for levelA in root:
        for levelB in levelA:
            ident = levelB.get('SERIES_NAME')
            if ident in [name]:
                for levelC in levelB[1:-1]:
                    v = levelC.get('OBS_VALUE')
                    d= levelC.get('TIME_PERIOD')
                    dates = np.append(dates,d)
                    value = np.append(value,float(v))

    for n,d in enumerate(dates):
        dates[n]= datetime.datetime.strptime(d, '%Y-%m-%d').strftime('%m-%d-%Y')
        
    df = pd.DataFrame(value,index=dates)
    return df


tree = etree.parse("Z1_data.xml")
root = tree.getroot()

# legend= createLegend(root)

tBills = getSeries('FL313161113.A')
tBills.plot()
plt.show()