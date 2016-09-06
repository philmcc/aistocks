#!/usr/bin/python
# -*- coding: utf-8 -*-

import MySQLdb as mdb
from pyfann import libfann
from datetime import date
from network_functions import save_prediction

mydate = date.today()

con = None
con = mdb.connect('localhost', 'root',
        'fil1202job', 'stock');

with con:
    cur = con.cursor(mdb.cursors.DictCursor)
    cur1 = con.cursor()
    cur2 = con.cursor()
    #
    # Get a list of all networks
    #
    cur.execute("SELECT a.id, a.group, b.ticker, b.predict_data, a.net_file FROM `network`.`network` a, network.net_group b where a.group = b.id;")
    rows = cur.fetchall()

    for row in rows:
        #
        # For each network get the training data - only most recent data at the moment
        #
        #seldate = "select latest_prediction from network.network where id = " + str(row["id"])
        #cur2.execute(seldate)
        #latestdate = cur2.fetchone()
        #latestdate1 = latestdate[0]

        #print latestdate1
        cur1.execute(row["predict_data"])
        for row1 in cur1.fetchall():
            #
            # Extract Date
            #
            mydate = row1[(len(row1) - 1)]
            row1b = list(row1)
            del row1b[(len(row1b) - 1)]
            #
            # Set up network
            #
            ann = libfann.neural_net()
            ann.create_from_file(row["net_file"])
            #
            # Run Prediction
            #
            print ann.run(row1b)
            prediction = ann.run(row1b)
            prediction = str(prediction).translate(None, '[]')
            #
            # Store results in db - Function
            #
            save_prediction(row["id"], mydate, prediction)


