#!/usr/bin/python
# -*- coding: utf-8 -*-

import MySQLdb as mdb




con = None
con = mdb.connect('localhost', 'root', 'fil1202job', 'stock')

cursor = con.cursor()
sql = "SELECT id, qdate from stock.stocks where stocks.NDC is NULL;"
print sql
cursor1 = con.cursor()

cursor.execute(sql)
for row in cursor.fetchall():
    print sql
    sql2 = "select stocks.close from stock.stocks where stocks.qdate > \"" + str(row[1]) + "\" order by qdate asc limit 1"
    cursor2 = con.cursor()
    cursor2.execute(sql2)
    for row2 in cursor2.fetchall():
        sql3 = "update stock.stocks set stocks.NDC = " + str(row2[0]) + "where id = " + str(row[0])
        cursor3 = con.cursor()
        cursor3.execute(sql3)

con.commit()
con.close()
