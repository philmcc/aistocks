#!/usr/bin/python

#
# Picks a type then a group and creates 5 networks for that group with varying parameters
#

from network_functions import create_group
from network_functions import create_net
from network_functions import calc_test_accuracy
import MySQLdb as mdb

con = mdb.connect('localhost', 'root', 'fil1202job', 'network')

cursor = con.cursor()
sql = "select distinct(id) from network.net_type;"

cursor1 = con.cursor()


cursor.execute(sql)
for row in cursor.fetchall():
    print "Net Type is " + str(row[0])
    net_type = row[0]
    sql1 = "Select ticker from stock.tickers where ticker not in (select distinct(ticker) from network.net_group where type = "+ str(row[0]) + ")"

    # Execute the SQL command
    cursor1.execute(sql1)
    for row1 in cursor1.fetchall():
        print "ticker without net " + row1[0]
        ticker = row1[0]
        #For each ticker call create group
        create_group(net_type, ticker)



    #select count(a.id), a.group from network.network a group by a.group order by count(a.id) desc;
cursor2 = con.cursor()
sql2 = "select a.id from network.net_group a where a.id not in (select distinct(b.group) from network.network b)"
    #for first group, create 5 networks
cursor2.execute(sql2)
counter = 0
for row2 in cursor2.fetchall():
    if counter < 1000:
        create_net(row2[0], 14)
        create_net(row2[0], 10)
        create_net(row2[0], 15)
        create_net(row2[0], 9)
        create_net(row2[0], 8)
    counter = counter + 1

test = calc_test_accuracy()








