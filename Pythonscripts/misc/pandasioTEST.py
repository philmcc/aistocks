from pandas.io.data import DataReader
from datetime import datetime
from pandas import *
import pandas
pandas.set_printoptions(max_rows=2000, max_columns=14)
#from talib import abstract
import talib
#msft = DataReader("MSFT",  "yahoo")
#msft = DataReader("MSFT",  "yahoo", datetime(2009,1,1))
#print msft["Volume"]
#print msft["Adj Close"][-100:]
#print msft
vticker = "GOOG"
goog = DataReader(vticker,  "yahoo", datetime(2009,1,1))
#print goog["Close"]
#print goog

#goog2 = goog["Close"].shift(1, freq=datetools.bday)

#goog2 = goog + goog
#print goog2.index

#pandas.set_printoptions(max_rows=2000, max_columns=10)

## Calculate NDC and Previous closes
goog["NDC"] =  goog["Close"].shift(-1)
goog["close-1"] =  goog["Close"].shift(1)
goog["close-2"] =  goog["Close"].shift(2)
goog["close-3"] =  goog["Close"].shift(3)
goog["close-4"] =  goog["Close"].shift(4)
goog["close-5"] =  goog["Close"].shift(5)
goog["close-6"] =  goog["Close"].shift(6)
goog["close-7"] =  goog["Close"].shift(7)
goog["close-8"] =  goog["Close"].shift(8)
goog["close-9"] =  goog["Close"].shift(9)
goog["close-10"] =  goog["Close"].shift(10)
#goog["close-11"] =  goog["Close"].shift(11)
#goog["close-12"] =  goog["Close"].shift(12)
#goog["close-13"] =  goog["Close"].shift(13)
#goog["close-14"] =  goog["Close"].shift(14)
#goog["close-15"] =  goog["Close"].shift(15)
#goog["close-16"] =  goog["Close"].shift(16)
#goog["close-17"] =  goog["Close"].shift(17)
#goog["close-18"] =  goog["Close"].shift(18)
#goog["close-19"] =  goog["Close"].shift(19)
#goog["close-20"] =  goog["Close"].shift(20)

goog["Open-1"] =  goog["Open"].shift(1)
goog["Open-2"] =  goog["Open"].shift(2)
goog["Open-3"] =  goog["Open"].shift(3)
goog["Open-4"] =  goog["Open"].shift(4)
goog["Open-5"] =  goog["Open"].shift(5)
goog["Open-6"] =  goog["Open"].shift(6)
goog["Open-7"] =  goog["Open"].shift(7)
goog["Open-8"] =  goog["Open"].shift(8)
goog["Open-9"] =  goog["Open"].shift(9)
goog["Open-10"] =  goog["Open"].shift(10)

goog["High-1"] =  goog["High"].shift(1)
goog["High-2"] =  goog["High"].shift(2)
goog["High-3"] =  goog["High"].shift(3)
goog["High-4"] =  goog["High"].shift(4)
goog["High-5"] =  goog["High"].shift(5)
goog["High-6"] =  goog["High"].shift(6)
goog["High-7"] =  goog["High"].shift(7)
goog["High-8"] =  goog["High"].shift(8)
goog["High-9"] =  goog["High"].shift(9)
goog["High-10"] =  goog["High"].shift(10)

goog["Low-1"] =  goog["Low"].shift(1)
goog["Low-2"] =  goog["Low"].shift(2)
goog["Low-3"] =  goog["Low"].shift(3)
goog["Low-4"] =  goog["Low"].shift(4)
goog["Low-5"] =  goog["Low"].shift(5)
goog["Low-6"] =  goog["Low"].shift(6)
goog["Low-7"] =  goog["Low"].shift(7)
goog["Low-8"] =  goog["Low"].shift(8)
goog["Low-9"] =  goog["Low"].shift(9)
goog["Low-10"] =  goog["Low"].shift(10)

goog["Volume-1"] =  goog["Volume"].shift(1)
goog["Volume-2"] =  goog["Volume"].shift(2)
goog["Volume-3"] =  goog["Volume"].shift(3)
goog["Volume-4"] =  goog["Volume"].shift(4)
goog["Volume-5"] =  goog["Volume"].shift(5)
goog["Volume-6"] =  goog["Volume"].shift(6)
goog["Volume-7"] =  goog["Volume"].shift(7)
goog["Volume-8"] =  goog["Volume"].shift(8)
goog["Volume-9"] =  goog["Volume"].shift(9)
goog["Volume-10"] =  goog["Volume"].shift(10)

#print goog
#print goog.to_string()

## Calculate SMA's'
goog["SMA5"] = talib.SMA(goog["Close"], 5)
goog["SMA10"] = talib.SMA(goog["Close"], 10)
goog["SMA15"] = talib.SMA(goog["Close"], 15)
goog["SMA20"] = talib.SMA(goog["Close"], 20)
goog["SMA50"] = talib.SMA(goog["Close"], 50)
goog["SMA100"] = talib.SMA(goog["Close"], 100)
goog["SMA200"] = talib.SMA(goog["Close"], 200)

## Calculate EMA's'
goog["EMA5"] = talib.EMA(goog["Close"], 5)
goog["EMA10"] = talib.EMA(goog["Close"], 10)
goog["EMA15"] = talib.EMA(goog["Close"], 15)
goog["EMA20"] = talib.EMA(goog["Close"], 20)
goog["EMA50"] = talib.EMA(goog["Close"], 50)
goog["EMA100"] = talib.EMA(goog["Close"], 100)
goog["EMA200"] = talib.EMA(goog["Close"], 200)

# Predictive indicators
#goog["v2crows"] = talib.CDL2CROWS(goog["Open"], goog["High"], goog["Low"], goog["Close"])
#goog["v3blackcrows"] = talib.CDL3BLACKCROWS(goog["Open"], goog["High"], goog["Low"], goog["Close"])
#goog["vCDL3INSIDE"] = talib.CDL3INSIDE(goog["Open"], goog["High"], goog["Low"], goog["Close"])
#goog["vCDL3LINESTRIKE"] = talib.CDL3LINESTRIKE(goog["Open"], goog["High"], goog["Low"], goog["Close"])
#goog["vCDL3OUTSIDE"] = talib.CDL3OUTSIDE(goog["Open"], goog["High"], goog["Low"], goog["Close"])

#goog["HT_TRENDMODE"] = talib.HT_TRENDMODE(goog["Close"])


rev_goog = goog.sort(ascending=0)
#result = df.sort(['A', 'B'], ascending=[1, 0])
#print rev_goog.to_string()
#rev_goog2 = rev_goog[:5]#.to_string()

#for row_index, row in rev_goog.iterrows():
    #print row.T
    #print '%s\n%s' % (row_index, row)
print rev_goog.to_string()

#print rev_goog.ix["2013-03-01"]

#df2_t = DataFrame(dict((idx,values) for idx, values in rev_goog.iterrows()))
#print df2_t.T

import MySQLdb as mdb

con = mdb.connect('localhost', 'root', 'fil1202job', 'network')
cursor = con.cursor()

for r in rev_goog2.itertuples(): #
#    sql = "INSERT INTO `stock`.`stock_test` (`qdate`, `ticker`, `open`) VALUES (\""+ str(r[0]) + "\", \"" + vticker + "\", " + str(r[1]) + ")"
    try:
        print sql
#        cursor.execute(sql)
    except:
        con.rollback()
con.commit()
con.close()


