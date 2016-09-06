#!/usr/bin/python
# -*- coding: utf-8 -*-

import MySQLdb as mdb

con = None
con = mdb.connect('localhost', 'root',
        'fil1202job', 'network');

cursor = con.cursor()
# Prepare SQL query to INSERT a record into the database.
sql = "INSERT INTO network.net_group(type, ticker) VALUES ( 3, 'ACN');"

try:
   # Execute the SQL command
   cursor.execute(sql)
   # Commit your changes in the database
   con.commit()
except:
   # Rollback in case there is any error
   con.rollback()

# disconnect from server
con.close()
