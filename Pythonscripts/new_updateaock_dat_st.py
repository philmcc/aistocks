#import ystockquote
import MySQLdb as mdb
import datetime
from network_functions import update_ndc
from pandas.io.data import DataReader
from pandas import *
import pandas
import talib
#print datetime.date.today()


#vtoday = datetime.date.today()
#vtodaysdate = vtoday.strftime('%Y%m%d')

con = None
con = mdb.connect('localhost', 'root','fil1202job', 'stock');
cur = con.cursor()
cur2 = con.cursor()
cur3 = con.cursor()
sql = "select distinct(ticker) from stock.tickers"
vsdate =  "20130301"

cur.execute(sql)
tickers = cur.fetchall()
count=0
for ticker in tickers:

    if count < 100:
        print str(ticker[0])
        sql2 = "select ifnull(date_format(max(qdate),'%Y%m%d'),'20040601') from stock.stock_new where ticker = \"" + str(ticker[0]) + "\""
        cur2.execute(sql2)
        vsdate = cur2.fetchone()

        goog = DataReader(ticker[0],  "yahoo", datetime(2000,1,1))
        ## Calculate NDC and Previous closes
        goog["NDC"] =  goog["Close"].shift(-1)           #7
        goog["close-1"] =  goog["Close"].shift(1)        #8
        goog["close-2"] =  goog["Close"].shift(2)        #8
        goog["close-3"] =  goog["Close"].shift(3)        #9
        goog["close-4"] =  goog["Close"].shift(4)        #10
        goog["close-5"] =  goog["Close"].shift(5)        #11
        goog["close-6"] =  goog["Close"].shift(6)        #12
        goog["close-7"] =  goog["Close"].shift(7)        #13
        goog["close-8"] =  goog["Close"].shift(8)        #14
        goog["close-9"] =  goog["Close"].shift(9)        #15
        goog["close-10"] =  goog["Close"].shift(10)        #16

        goog["Open-1"] =  goog["Open"].shift(1)        #17
        goog["Open-2"] =  goog["Open"].shift(2)        #18
        goog["Open-3"] =  goog["Open"].shift(3)        #19
        goog["Open-4"] =  goog["Open"].shift(4)        #20
        goog["Open-5"] =  goog["Open"].shift(5)        #21
        goog["Open-6"] =  goog["Open"].shift(6)        #22
        goog["Open-7"] =  goog["Open"].shift(7)        #23
        goog["Open-8"] =  goog["Open"].shift(8)        #24
        goog["Open-9"] =  goog["Open"].shift(9)        #25
        goog["Open-10"] =  goog["Open"].shift(10)        #26

        goog["High-1"] =  goog["High"].shift(1)        #27
        goog["High-2"] =  goog["High"].shift(2)        #28
        goog["High-3"] =  goog["High"].shift(3)        #29
        goog["High-4"] =  goog["High"].shift(4)        #30
        goog["High-5"] =  goog["High"].shift(5)        #31
        goog["High-6"] =  goog["High"].shift(6)        #32
        goog["High-7"] =  goog["High"].shift(7)        #33
        goog["High-8"] =  goog["High"].shift(8)        #34
        goog["High-9"] =  goog["High"].shift(9)        #35
        goog["High-10"] =  goog["High"].shift(10)        #36

        goog["Low-1"] =  goog["Low"].shift(1)        #37
        goog["Low-2"] =  goog["Low"].shift(2)        #38
        goog["Low-3"] =  goog["Low"].shift(3)        #39
        goog["Low-4"] =  goog["Low"].shift(4)        #40
        goog["Low-5"] =  goog["Low"].shift(5)        #41
        goog["Low-6"] =  goog["Low"].shift(6)        #42
        goog["Low-7"] =  goog["Low"].shift(7)        #43
        goog["Low-8"] =  goog["Low"].shift(8)        #44
        goog["Low-9"] =  goog["Low"].shift(9)        #45
        goog["Low-10"] =  goog["Low"].shift(10)        #46

        goog["Volume-1"] =  goog["Volume"].shift(1)    #47
        goog["Volume-2"] =  goog["Volume"].shift(2)    #48
        goog["Volume-3"] =  goog["Volume"].shift(3)    #49
        goog["Volume-4"] =  goog["Volume"].shift(4)    #50
        goog["Volume-5"] =  goog["Volume"].shift(5)    #51
        goog["Volume-6"] =  goog["Volume"].shift(6)    #52
        goog["Volume-7"] =  goog["Volume"].shift(7)    #53
        goog["Volume-8"] =  goog["Volume"].shift(8)    #54
        goog["Volume-9"] =  goog["Volume"].shift(9)    #55
        goog["Volume-10"] =  goog["Volume"].shift(10)    #56

        ## Calculate SMA's'
        goog["SMA5"] = talib.SMA(goog["Close"], 5)        #57
        goog["SMA10"] = talib.SMA(goog["Close"], 10)        #58
        goog["SMA15"] = talib.SMA(goog["Close"], 15)        #59
        goog["SMA20"] = talib.SMA(goog["Close"], 20)        #60
        goog["SMA50"] = talib.SMA(goog["Close"], 50)        #61
        goog["SMA100"] = talib.SMA(goog["Close"], 100)        #62
        goog["SMA200"] = talib.SMA(goog["Close"], 200)        #63

        ## Calculate EMA's'
        goog["EMA5"] = talib.EMA(goog["Close"], 5)        #64
        goog["EMA10"] = talib.EMA(goog["Close"], 10)        #65
        goog["EMA15"] = talib.EMA(goog["Close"], 15)        #66
        goog["EMA20"] = talib.EMA(goog["Close"], 20)        #67
        goog["EMA50"] = talib.EMA(goog["Close"], 50)        #68
        goog["EMA100"] = talib.EMA(goog["Close"], 100)        #69
        goog["EMA200"] = talib.EMA(goog["Close"], 200)        #72

        goog["maxopen"] = talib.max(goog["open"], 60)        #72
        goog["maxclose"] = talib.max(goog["Close"], 60)        #72
        goog["maxhigh"] = talib.max(goog["high"], 60)        #72
        goog["maxlow"] = talib.max(goog["low"], 60)        #72
        goog["maxvol"] = talib.max(goog["volume"], 60)        #72


        rev_goog = goog.sort(ascending=0)
        rev_goog2 = rev_goog[:2500]#.to_string()
        counter = 0
        #for quote in rev_goog2:
        for quote in rev_goog2.itertuples():
            if counter > 0:
                #print len(quote)
                #for i in range(0, len(quote)):
                #    print quote[i]
                #print quote
                sql3 = "INSERT INTO `stock`.`stock_new` (`ticker`, `qdate`, `open`, `high`, `low`, `close`, `volume`, `adj_Close`, `NDC`, `close_1`, `close_2`, `close_3`,  `close_4`, `close_5`, `close_6`, `close_7`, `close_8`, `close_9`, `close_10`, `Open_1`, `Open_2`, `Open_3`, `Open_4`, `Open_5`, `Open_6`, `Open_7`, `Open_8`, `Open_9`, `Open_10`, `High_1`, `High_2`, `High_3`, `High_4`, `High_5`, `High_6`, `High_7`,  `High_8`, `High_9`, `High_10`, `Low_1`, `Low_2`,`Low_3`, `Low_4`, `Low_5`, `Low_6`, `Low_7`, `Low_8`, `Low_9`, `Low_10`, `Volume_1`, `Volume_2`, `Volume_3`, `Volume_4`, `Volume_5`, `Volume_6`, `Volume_7`, `Volume_8`, `Volume_9`, `Volume_10`, `SMA5`, `SMA10`, `SMA15`, `SMA20`, `SMA50`, `sMA100`, `SMA200`, `EMA5`, `EMA10`, `EMA15`, `EMA20`, `EMA50`, `EMA100`, `EMA200`) VALUES ("
                sql3 = sql3 + "\"" + str(ticker[0])
                sql3 = sql3 + "\", \""  + str(quote[0]) + "\""
                #sql3 = sql3 + ", " + str(quote[1]) + ", " + str(quote[2]) + ", " + str(quote[3]) + ", " + str(quote[4]) + ", " + str(quote[5]) + ", " + str(quote[6]) + ", " + str(quote[7]) + ", " + str(quote[8]) + ", " + str(quote[9]) + ", " + str(quote[10]) + ", " + str(quote[11]) + ", " + str(quote[12]) + ", " + str(quote[13]) + ", " + str(quote[14]) + ", " + str(quote[15]) + ", " + str(quote[16]) + ", " + str(quote[17]) + ", " + str(quote[18]) + ", " + str(quote[19]) + ", " + str(quote[20]) + ", " + str(quote[21]) + ", " + str(quote[22]) + ", " + str(quote[23]) + ", " + str(quote[24]) + ", " + str(quote[25]) + ", " + str(quote[26]) + ", " + str(quote[27]) + ", " + str(quote[28]) + ", " + str(quote[29]) + ", " + str(quote[30]) + ", " + str(quote[31]) + ", " + str(quote[32]) + ", " + str(quote[33]) + ", " + str(quote[34]) + ", " + str(quote[35]) + ", " + str(quote[36]) + ", " + str(quote[37]) + ", " + str(quote[38]) + ", " + str(quote[39]) + ", " + str(quote[40]) + ", " + str(quote[41]) + ", " + str(quote[42]) + ", " + str(quote[43]) + ", " + str(quote[44]) + ", " + str(quote[45]) + ", " + str(quote[46]) + ", " + str(quote[47]) + ", " + str(quote[48]) + ", " + str(quote[49]) +  ", " + str(quote[50]) + ", " + str(quote[51]) + ", " + str(quote[52]) + ", " + str(quote[53]) + ", " + str(quote[54]) + ", " + str(quote[55]) + ", " + str(quote[56]) + ", " + str(quote[57]) + ", " + str(quote[58]) + ", " + str(quote[59]) + ", " + str(quote[60]) + ", " + str(quote[61]) + ", " + str(quote[62]) + ", " + str(quote[63]) + ", " + str(quote[64]) + ", " + str(quote[65]) + ", " + str(quote[66]) + ", " + str(quote[67]) + ", " + str(quote[68]) + ", " + str(quote[69]) + ", " + str(quote[70]) + ", " + str(quote[71])+  ")"

                for x in range(1,71):
                    if str(quote[x]) = "nan":
                        sql3 = sql3 + ", NULL"
                    else:
                        sql3 = sql3 + ", " + str(quote[x])
                sql3 = sql3 + ")"
                #print sql3
                try:
                   cur3.execute(sql3)
                   #print "test"
                   #print "\n"
                except:
                   #Rollback in case there is any error
                   con.rollback()
                   print sql3
                   print con.info()
                   print " error"
            con.commit()
            counter = counter +1
        print counter
        count = count + 1

con.commit()
con.close()

#update_ndc()

