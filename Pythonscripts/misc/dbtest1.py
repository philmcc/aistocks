#!/usr/bin/python
# -*- coding: utf-8 -*-

import MySQLdb as mdb
import sys

con = None

con = mdb.connect('11.36.0.14', 'philmcc_network', 'fil1202job', 'network')


cur = con.cursor()
cur.execute("SELECT * FROM `network_test`")

resultsrow = ""

for row in cur.fetchall() :
    for i in range(len(row)):
        print row[i]
        print i
        if i == 0:
            resultsrow = resultsrow + row[i]
        else:
            resultsrow = resultsrow + ", " + str(row[i])
        print resultsrow
print "Done"""

