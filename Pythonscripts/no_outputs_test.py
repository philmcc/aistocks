#!/usr/bin/python

import MySQLdb as mdb

print "SAVE Prediction"

net_id = 36

con = None
con = mdb.connect('localhost', 'root', 'fil1202job', 'network')

sql_outputs = "SELECT c.no_output FROM network.network a, network.net_group b, network.net_type c where c.id = b.type and b.id = a.group and a.id = " + str(net_id)
sql_cur = con.cursor()
sql_cur.execute(sql_outputs)
no_outputs = sql_cur.fetchone()

if int(no_outputs[0]) == 1:
    print "its 1"
else:
    print "its not 1"
