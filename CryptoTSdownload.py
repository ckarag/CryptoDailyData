# -*- coding: utf-8 -*-
"""
Use the Coinpaprika API to download all the DAILY timeseries Open/High/Low/Close, 
Volume & Market Cap for all the available crypto tickers (11027 as of March 2022).
Saves in two separate .csv files: (1) the list containing all the tickers (coinpaprika_tickers.csv)
and (2) the list containing all the coins (coinpaprika_coins.csv). All series are quoted in USD.
NB: The code downloads and saves (in the working directory) one csv file for every ticker. 
@author: Haris Karagiannakis (https://github.com/ckarag)
"""

#FUNCTION candles()
#Return Open/High/Low/Close and Volume & Market Cap. on daily frequency, with a max of 366 rows
#c.candles("btc-bitcoin", start="2019-01-11", end="2022-01-11")

pip install coinpaprika
from coinpaprika import client as Coinpaprika
c = Coinpaprika.Client() #API Client

import pandas as pd

#######################
# List of ALL TICKERS #
#######################
tic = c.tickers() #Get tickers for ALL coins (USD,BTC,ETH)

id=[]
name=[]
symbol=[]
Dstr=[]
Dend=[]
Dendtime = []
rnk=[]
for i in range(0, len(tic)):
    print('iter: ' + str(i))
    
    id.append(tic[i]['id'])
    name.append(tic[i]['name'])
    symbol.append(tic[i]['symbol'])
    
    #START DATE
    #The date is a string of the form: '2021-03-30T00:00:00Z'
    strdayonly = tic[i]['first_data_at'][0:10] 
    Dstr.append(strdayonly)

    #END DATE
    endall = tic[i]['last_updated']
    k = endall.split('T')
    Dend.append(k[0])
    Dendtime.append(k[1])
    
    rnk.append(tic[i]['rank'])
print("Finished!")
    
dict = {'id': id, 'name': name, 'symbol': symbol, 'Dstr': Dstr, 'Dend': Dend, 'Dendtime':Dendtime, 'rnk': rnk}
df_t = pd.DataFrame(dict)
	
# save in csv
df_t.to_csv('coinpaprika_tickers.csv')


#####################
# List of ALL COINS #
#####################
tic = c.coins() #Get list of ALL coins

id=[]
name=[]
symbol=[]
rnk=[]
is_active = []
type = []
for i in range(0, len(tic)):
    print('iter: ' + str(i))
    
    id.append(tic[i]['id'])
    name.append(tic[i]['name'])
    symbol.append(tic[i]['symbol'])
    rnk.append(tic[i]['rank'])
    is_active.append(tic[i]['is_active'])
    type.append(tic[i]['type'])
print("Finished!")
    
dict = {'id': id, 'name': name, 'symbol': symbol, 'rnk': rnk, 'is_active': is_active, 'type': type}
df_c = pd.DataFrame(dict)
	
# save in csv
df_c.to_csv('coinpaprika_coins.csv')

del endall, Dstr, Dend, Dendtime, i, id, dict, is_active, k, name, rnk, strdayonly, symbol, type, tic



#########################
## Download Timeseries ##
#########################

for i in range(0, len(tic)): #Loop over tickers
    ts_tic = pd.DataFrame([])
    tsfrm = int(df_t.loc[i,'Dstr'][0:4])
    tsto = int(df_t.loc[i,'Dend'][0:4])
    
    for j in range(tsfrm, tsto+1): #Loop over the different available years
        print('iter: ' + str(i))
        strdate = str(j) + "-01-01"
        tstmp = c.candles(tic[i]['id'], start=strdate, limit=366) #Download OHLCV 366 daily obs 
        tstmp = pd.DataFrame(tstmp)
        ts_tic = pd.concat([ts_tic, tstmp], sort=False) #Append the different years

    #tickername = df_t.loc[i,'id']
    tickername = df_t.loc[i,'symbol']
    ts_tic = ts_tic.drop_duplicates() #Remove duplicate rows (due to concatenation)
    
    pathname = tickername + '.csv'
    ts_tic.to_csv(pathname, index=False)

del ts_tic, tsfrm, tsto, tickername, pathname, i, j, tstmp, strdate
