# Economic Data
Python programs for downloading economic data and constructing data sets. Contents of the main directories in this repo are described below.

## `business-cycle-data`

Code for downloading and managing data about the US business cycle to use as resources for my Computational Macroeconomics class at UC, Irvine. Four data sets are exported. Two contain only real variables and are used to support RBC analysis. The next two contain nominal variables like inflation and the T-Bill rate and unemployment and is used to miotivate a new Keynesian perspective.

## `covered-interest-parity`
Construct data sets containing spot and forward exchange rates and interest rates for the Japanes yen, Swiss franc, and US dollar. Code is in the `python` directory and exports data to `csv` and `xslx` directories.

## `cross-country-production`

Program for constructing csv files containing real GDP per capita and other indicators from 1960 to present including every country for which data is available for every year. Original data is from the Penn World Tables (https://www.rug.nl/ggdc/productivity/pwt/).
     
## `dmp`

Construct a data set containing labor and vacancy statistics for the US from 1929 to the most recenlty available.
 
## `historical-statistics-of-the-us`

Historial data on:

* bank suspensions: annual, 1864 - 1970
* gross national product and deflator: annual, 1889 - 1970
* components of the money stock annual: 1889 - 1970
* unemployment: annual, 1890 - 1970

Source: https://www.census.gov/library/publications/1975/compendia/hist_stats_colonial-1970.html

## `inflation-forecasts`

Download and manage inflation forecast data from the Survey of Professional Forecasters (https://www.philadelphiafed.org/surveys-and-data/real-time-data-research/survey-of-professional-forecasters).

## `oecd-unemployment`

Download, manage, and export international unemployment data. Primary data source: https://data.oecd.org/unemp/harmonised-unemployment-rate-hur.htm

## `quantity-theory`

Program for constructing datasets including long-run average rates of money (M1) growth, real GDP growth, and CPI inflation for each country for which there is at least 10 years of continuously available data for each variable. Data is downloaded from the World Bank World Development Indicators using the wbdata api.

## `real-rate`

Program for constructing a dataset that includes the 1-year T-bill rate, the 1-year ahead inflation forecast from the Survey of Professional Forecasters reported by the Federal Reserve Bank of Philadelphia, the 1-year ahead actual rate of inflation, and the one-year ahead actual growth rate in real consumption expenditures for the US. The data are from 1971.

## `sargent1982`

Data from Sargent's 1982 chapter "The Ends of Four Big Inflations": https://www.nber.org/system/files/chapters/c11452/c11452.pdf

## `seigniorage`

Generates seigniorage data for the US

## `sifma`

Financial data from SIFMA on outstanding mortgage-backed securities.

## `us-convergence`

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
