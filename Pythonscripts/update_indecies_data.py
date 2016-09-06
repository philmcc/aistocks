#!/usr/bin/python

    import ystockquote
    import MySQLdb as mdb
    import datetime
    from network_functions import update_ndc

    print datetime.date.today()
    vtoday = datetime.date.today()
    vtodaysdate = vtoday.strftime('%Y%m%d')

    con = None
    con = mdb.connect('localhost', 'root','fil1202job', 'stock');
    cur = con.cursor()
    cur2 = con.cursor()
    cur3 = con.cursor()
    sql = "select distinct(ticker) from stock.indecies"
    vsdate =  "20130301"

    cur.execute(sql)
    tickers = cur.fetchall()
    count=0
    for ticker in tickers:
        if count < 10000:
            sql2 = "select ifnull(date_format(max(qdate),'%Y%m%d'),'20040601') from stock.indecies_data where ticker = \"" + str(ticker[0]) + "\""
            cur2.execute(sql2)
            vsdate = cur2.fetchone()
            #vstartdate = vsdate[0]
            #vstartdate = datetime.datetime.strptime(vsdate[0], "%Y%m%d")
            #vstartdate = vstartdate + datetime.timedelta(days=1)
            #print vstartdate.strftime('%Y%m%d')
            quotes = ystockquote.get_historical_prices(ticker[0], vsdate[0], vtodaysdate)
            print "#####"
            print ticker[0]

            counter = 0
            for quote in quotes:
                if counter > 0:
                    #print quote
                    sql3 = "INSERT INTO `stock`.`indecies_data` (`ticker`,`qdate`,`open`,`high`,`low`,`close`,`volume`) VALUES(\"" + str(ticker[0]) + "\", \"" + quote[0] + "\", " + quote[1] + ", " + quote[2] + ", " + quote[3] + ", " + quote[4] + ", " + quote[5] + ")"
                    try:
                        cur3.execute(sql3)
                    except:
                        # Rollback in case there is any error
                        con.rollback()
                        #print " error"
                counter = counter +1
            print counter
            count = count + 1

    con.commit()
    con.close()



