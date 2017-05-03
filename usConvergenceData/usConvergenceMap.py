
# coding: utf-8

# In[1]:

from __future__ import division
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as dts
import pandas as pd
import statsmodels.api as sm
from bs4 import BeautifulSoup
import subprocess,os
import runProcs
# get_ipython().magic('matplotlib inline')


# In[2]:

# -1.0 Create an svg map using the simplemapplot package

# If the map file usMap.svg is not available locally uncomment the following.
# Note that simplemapplot is not compatible with python 3.

# import simplemapplot
# simplemapplot.make_us_state_map({"GA":0},colors=['#7FA9CF'],output_img='usMap.svg')
svg = open('usMap.svg', 'r').read()


# In[3]:

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


# In[4]:

# 1. Load and manage income data

# 1.1 Load state income csv file and convert income to 1000s of dollars
stateIncome = pd.read_csv('stateIncomeData.csv',index_col=0)
stateIncome = stateIncome/1000
stateIncome = stateIncome.sort_index(axis=0, ascending=True)

#1.2 Create a US series and drop us from state set
usIncome = stateIncome[u'United States']
stateIncome = stateIncome.drop([u'United States'],axis=1)

# 1. List of the Confederate states
csa = ['SC','MS','FL','AL','GA','LA','TX','VA','AR','TN','NC']

stateIncome.index


# In[5]:

# 2. Compute statistics

stateIncomeFrom1929 = stateIncome.iloc[3:]

# 2.1 Per capita income at start of sample
origY = stateIncomeFrom1929.iloc[0]

# 2.2 Compute average annual growth rates over sample
T = len(stateIncomeFrom1929.index)-1
growth = []
for i in stateIncomeFrom1929.columns:
    growth.append( 100*1/T*(np.log(stateIncomeFrom1929[i].iloc[-1]/stateIncomeFrom1929[i].iloc[0])))

# 2.3 OLS regression
X = sm.add_constant(origY)

model = sm.OLS(growth,X)
results = model.fit()
results.params

slope = results.params[0]
inter = results.params[1]


# In[6]:

# 3.1 Plots

# 3. Plot the growth - initial income relationship
fig = plt.figure()
ax = fig.add_subplot(1, 1, 1)


for i,state in enumerate(stateIncome.columns):
    if state in csa:
        plt.text(origY[i], growth[i], state, color="red",fontsize=12, clip_on=True,horizontalalignment='center',verticalalignment='center',alpha = 1)
    else:
        plt.text(origY[i], growth[i], state, color="#11557c",fontsize=12, clip_on=True,horizontalalignment='center',verticalalignment='center',alpha = 1)

ax.plot(np.arange(0,20,0.001),inter+slope*np.arange(0,20,0.001),'-k')
ax.set_ylim([1,3.5])
ax.set_xlim([2,14])
ax.set_xlabel('income per capita in 1929 \n (thousands of 2009 $)')
ax.set_ylabel('average growth')
plt.grid()

plt.tight_layout()
plt.savefig('fig_us_statesIncomeGrowth.png',bbox_inches='tight',dpi=120)


# In[7]:

# 3.2 Plot income per capita in all states
fig = plt.figure()
ax = fig.add_subplot(1, 1, 1)


for i,state in enumerate(stateIncome.columns):
    if state not in csa:
        north = ax.plot(stateIncome.index,stateIncome[state],'-b',lw=1,alpha=0.5,label='Union')

    else:
        south = ax.plot(stateIncome.index,stateIncome[state],'-r',lw=2,label='South')

ax.set_xlim([stateIncome.index[0],stateIncome.index[-1]])
ax.locator_params(axis='x',nbins=5)
ax.set_ylabel('income per capita \n (thousands of 2009 $)')
ax.locator_params(axis='x',nbins=6)
plt.grid()


lns = north+south
labs = [l.get_label() for l in lns]
plt.legend(lns,labs,loc='upper left')


plt.tight_layout()
plt.savefig('fig_us_statesIncome.png',bbox_inches='tight',dpi=120)


# In[8]:

# 3.2 Plot income per capita in all states
fig = plt.figure()
ax = fig.add_subplot(1, 1, 1)


for i,state in enumerate(stateIncome.columns):
    if state not in csa:
        north = ax.plot(stateIncome.index,(stateIncome[state]/usIncome-1),'-b',lw=1,alpha=0.5,label='Union')

    else:
        south = ax.plot(stateIncome.index,(stateIncome[state]/usIncome-1),'-r',lw=2,label='South')

ax.set_xlim([stateIncome.index[0],stateIncome.index[-1]])
ax.locator_params(axis='x',nbins=5)
ax.set_ylabel('real income per capita \n relative US average')
ax.locator_params(axis='x',nbins=6)
plt.grid()


lns = north+south
labs = [l.get_label() for l in lns]
plt.legend(lns,labs,loc='upper right',ncol=2)


plt.tight_layout()
plt.savefig('fig_us_statesIncomeRelative.png',bbox_inches='tight',dpi=120)


# In[9]:

# 4. Make the maps. Reference: http://flowingdata.com/2009/11/12/how-to-make-a-us-county-thematic-map-using-free-tools/

# 4.1.1 Specify a color scheme. Reference: http://colorbrewer2.org/
# colors=[,'#fcc5c0','#fa9fb5','#f768a1','#dd3497','#ae017e','#7a0177','#49006a']
colors=['#d4b9da','#c994c7','#df65b0','#e7298a','#ce1256','#980043','#67001f']
# colors=[#f1b6da','#fde0ef','#f7f7f7','#e6f5d0','#b8e186','#7fbc41','#4d9221']
# colors.reverse()

# 4.1.2 Specify the ranges of deviations of income from the us average for the color scheme
bins = [-.25,-.15,-.05,.05,.15,.25]
# bins = [-.45,-.25,-.1,-.05-.025,.025,.05,.1,.25,.45]


# In[10]:

# 4.2 Load svg with Beautiful Soup
soup = BeautifulSoup(svg, "lxml")
paths = soup.findAll('path')


# In[ ]:

# 4.3 Create color-coded maps for each year

path_style = 'font-size:12px;fill-rule:nonzero;stroke:#FFFFFF;stroke-opacity:1;stroke-width:0.1;stroke-miterlimit:4;stroke-dasharray:none;stroke-linecap:butt;marker-start:none;stroke-linejoin:bevel;fill:'
states = stateIncome.columns.tolist()
years = stateIncome.index.tolist()

for t,year in enumerate(stateIncome.index):
    for p in paths:
        if p['id'] in states or p['id']=='MI-' or p['id']=='SP-':
            if p['id']=='MI-' or p['id']=='SP-':
                i = states.index('MI')
            else:
                i = states.index(p['id'])
            y = ((stateIncome[states[i]].iloc[t]-usIncome.iloc[t])/usIncome.iloc[t])

            if y<bins[0]:
                color_class = 6
            elif bins[0]<=y<bins[1]:
                color_class = 5
            elif bins[1]<=y<bins[2]:
                color_class = 4
            elif bins[2]<=y<bins[3]:
                color_class = 3
            elif bins[3]<=y<bins[4]:
                color_class = 2
            elif bins[4]<=y<bins[5]:
                color_class = 1
            else:
                color_class = 0

            if np.isnan(y):
                color = '#D3D3D3'
                print(states[i])
            else:
                color = colors[color_class]
                
            p['style'] = path_style + color

    svg = soup.prettify()[17:56]+u'1054'+soup.prettify()[59:-24]
    svg = svg+u'<text style="font-size:50px" id="tcol0" x="600" y="560">'+str(year)+u'</text>\n'

    svg = svg+u'<text style="font-size:20px" id="tcol0" x="875" y="225">'+'Income per capita'+'</text>\n'
    svg = svg+u'<text style="font-size:20px" id="tcol0" x="875" y="250">'+'rel. to US avg.'+'</text>\n'
    
    svg = svg+u'<rect id="leg1" width="30" height="40" style="" x="875" y="260" fill="'+colors[0]+'"/>\n'
    svg = svg+u'<rect id="leg1" width="30" height="40" style="" x="875" y="300" fill="'+colors[1]+'"/>\n'
    svg = svg+u'<rect id="leg1" width="30" height="40" style="" x="875" y="340" fill="'+colors[2]+'"/>\n'
    svg = svg+u'<rect id="leg1" width="30" height="40" style="" x="875" y="380" fill="'+colors[3]+'"/>\n'
    svg = svg+u'<rect id="leg1" width="30" height="40" style="" x="875" y="420" fill="'+colors[4]+'"/>\n'
    svg = svg+u'<rect id="leg1" width="30" height="40" style="" x="875" y="460" fill="'+colors[5]+'"/>\n'
    svg = svg+u'<rect id="leg1" width="30" height="40" style="" x="875" y="500" fill="'+colors[6]+'"/>\n'

    svg = svg+u'<text style="font-size:20px" id="tcol0" x="915" y="290">above '+str(bins[5])+'</text>\n'
    svg = svg+u'<text style="font-size:20px" id="tcol0" x="915" y="330">'+str(bins[4])+' to '+str(bins[5])+'</text>\n'
    svg = svg+u'<text style="font-size:20px" id="tcol0" x="915" y="370">'+str(bins[3])+' to '+str(bins[4])+'</text>\n'
    svg = svg+u'<text style="font-size:20px" id="tcol0" x="915" y="410">'+str(bins[2])+' to '+str(bins[3])+'</text>\n'
    svg = svg+u'<text style="font-size:20px" id="tcol0" x="915" y="450">'+str(bins[1])+' to '+str(bins[2])+'</text>\n'
    svg = svg+u'<text style="font-size:20px" id="tcol0" x="915" y="490">'+str(bins[0])+' to '+str(bins[1])+'</text>\n'
    svg = svg+u'<text style="font-size:20px" id="tcol0" x="915" y="530"> below '+str(bins[0])+'</text>\n'
    
    svg = svg+soup.prettify()[-24:-17]
    
    svg = svg.split('<body>')[1]
    
    head = '<?xml version="1.0" encoding="UTF-8" standalone="no"?>\n<?xml-stylesheet href="Blank_US_Map.css" type="text/css"?>'
    svg = head + svg
    svg = svg.replace('width="959"','width="1035"')
    
    
    with open("images/stateRelativeIncome"+str(year)+".svg", "wb") as file:
        file.write(bytes(svg, 'UTF-8'))

    file = open("images/stateRelativeIncome"+str(year)+".svg", "a")
    convert = 'convert -density 144 images/stateRelativeIncome'+str(year)+'.svg images/stateRelativeIncome'+str(year)+'.png'
    subprocess.call(convert,shell=True)


# In[ ]:

# 4.4 Creat gif with imagemagick
makegif = 'convert -loop 0 -delay 50x100 images/*.png usStateConvergence.gif'
subprocess.call(makegif,shell=True)


# In[ ]:

# 5. Clean up
# os.chdir(os.getcwd())
# for files in os.listdir('.'):
#     if files.endswith('.css') or files.endswith('.svg'):
#         os.remove(files)


# In[ ]:

# 6. Export notebook to .py
runProcs.exportNb('usConvergenceMap')

