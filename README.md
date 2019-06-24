# Economic Data
Python programs for downloading economic data and constructing data sets.

## Covered Interest Parity
Construct data sets containing spot and forward exchange rates and interest rates for the Japanes yen, Swiss franc, and US dollar. Code is in the `python` directory and exports data to `csv` and `xslx` directories.

## Cross-Country Income
Program for constructing a .csv files containing real GDP per capita from 1970 to present including every country for which data is available for every year. Data is downloaded from the World Bank World Development Indicators using the wbdata api. 

  - Instructions: Run either `cross_country_income_data.ipynb`** or `cross_country_income_data.py`
  - Ouput to `csv` directory:
     - `cross_country_income.csv`: data in levels
     - `cross_country_income_log.csv` data in logs
     - A bunch of other data files.
     
 ## DMP
 Construct a data set containing labor and vacancy statistics for the US
 
 ## Historical Statistics of the US
 
 https://www.census.gov/library/publications/1975/compendia/hist_stats_colonial-1970.html

     

## quantityTheoryData
Program for constructing datasets including long-run average rates of money (M1) growth, real GDP growth, and CPI inflation for each country for which there is at least 10 years of continuously available data for each variable. Data is downloaded from the World Bank World Development Indicators using the wbdata api.

  - Instructions: Run either **quantityTheoryData.ipynb** or **quantityTheoryData.py**
  - Output: .csv files for all countries and for countries grouped by high, middle, and low income level.
    - qtyTheoryData.csv
    - qtyTheoryDataH.csv
    - qtyTheoryDataM.csv
    - qtyTheoryDataL.csv
  - Dependencies: wbdata, pandas, numpy, runProcs.py, qtyTheoryFunc.py

## realRateData
Program for constructing a dataset that includes the 1-year T-bill rate, the 1-year ahead inflation forecast from the Survey of Professional Forecasters reported by the Federal Reserve Bank of Philadelphia, the 1-year ahead actual rate of inflation, and the one-year ahead actual growth rate in real consumption expenditures for the US. The data are from 1971.

- Instructions: Run either **realRateData.ipynb** or **realRateData.py**
- Ouput: 
   - inflationForecastDataAnnual.csv
- Dependencies: pandas, numpy, runProcs.py, fredclass.py
  
## usConvergenceData
Programs for constucting a dataset of per capita income by US state and region from 1929 to the present and for constructing the of the data gif found on http://www.briancjenkins.com/data/usconvergence/.

1. US state income per capita dataset
  - Instructions: Run either **stateIncomeData.ipynb** or **stateIncomeData.py**
  - Ouput:
    - stateIncomeData.csv
  - Dependencies: numpy, pandas, json

2. US state income per capita animated gif.
  - Instructions: Run **usConvergenceMap.ipynb** or **usConvergenceMap.py**. *You must have ImageMagick (http://www.imagemagick.org/) installed on your system to run this.*
  - Output: 
    - usStateConvergence.gif
  - Dependencies: bs4 (BeautifulSoup), simplemapplot, runProcs.py
  
## usProductionData
Program for constructing a dataset for the US that includes real GDP, consumption, investment, government consumption, exports, imports, capital, and labor. The capital stock is constructed using the perpetual inventory method and there are some options for customizing the capital construction available in the program.

- Instructions: Run either **crossCountryIncomeData.ipynb** or **crossCountryIncomeData.py**
- Ouput: 
  - US_Production_A_Data.csv: Annual data, levels
  - US_Production_Q_Data.csv: Quarterly data, levels
  - US_Production_A_Data_Growth_Rates.csv: Annual data, growth rates
  - US_Production_Q_Data_Growth_Rates.csv: Quarterly data, growth rates 
- Dependencies: pandas, numpy, runProcs.py, fredclass.py

## z1data
Program for downloading the z.1 statistical release from the Federal Reserve and for parsing the xml file.
- Instructions: Run either **z1data.ipynb** or **z1data.py**
- Ouput: 
   - Z1legend.csv: csv file containing codes for each z.1 series (optional)
- Dependencies: pandas, numpy, requests, zipfile, lxml, runProcs.py
