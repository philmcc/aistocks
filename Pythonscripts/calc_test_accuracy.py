#!/usr/bin/python

import MySQLdb as mdb

con = mdb.connect('localhost', 'root', 'fil1202job', 'network')

cursor = con.cursor()
sql = "SELECT id FROM network.network where training_accuracy is null"

cursor1 = con.cursor()
#sql1 = "SELECT prediction, target FROM network.net_tests where net_id = " + str(vnet_id)

cursor3 = con.cursor()


cursor.execute(sql)
for row in cursor.fetchall():
    vnet_id = row[0]
    sql1 = "SELECT prediction, target FROM network.net_tests where net_id = " + str(vnet_id)

    vcounter = 0
    vcorrect = 0
    vincorrect = 0
    vaccuracy = 0
    vcounter5 = 0
    vcorrect5 = 0
    vincorrect5 = 0
    vaccuracy5 = 0
    vcounter9 = 0
    vcorrect9 = 0
    vincorrect9 = 0
    vaccuracy9 = 0

    cursor1.execute(sql1)
    for row1 in cursor1.fetchall():
        if float(row1[0]) > 0 and float(row1[1]) > 0:
            vcorrect = vcorrect + 1
        elif float(row1[0]) < 0 and float(row1[1]) < 0:
            vcorrect = vcorrect + 1
        else:
            vincorrect = vincorrect + 1
        vcounter = vcounter + 1


        if float(row1[0]) > 0.5:
            if float(row1[1]) == 1:
                vcorrect5 = vcorrect5 + 1
                vcounter5 = vcounter5 + 1
            else:
                vincorrect5 = vincorrect5 + 1
                vcounter5 = vcounter5 + 1
        elif float(row1[0]) < -0.5:
            if float(row1[1]) == -1:
                vcorrect5 = vcorrect5 + 1
                vcounter5 = vcounter5 + 1
            else:
                vincorrect5 = vincorrect5 + 1
                vcounter5 = vcounter5 + 1


        if float(row1[0]) > 0.9:
            if float(row1[1]) == 1:
                vcorrect9 = vcorrect9 + 1
                vcounter9 = vcounter9 + 1
            else:
                vincorrect9 = vincorrect9 + 1
                vcounter9 = vcounter9 + 1
        elif float(row1[0]) < -0.9:
            if float(row1[1]) == -1:
                vcorrect9 = vcorrect9 + 1
                vcounter9 = vcounter9 + 1
            else:
                vincorrect9 = vincorrect9 + 1
                vcounter9 = vcounter9 + 1


    vaccuracy = ((float(vcorrect) / float(vcounter)) *100)
    vaccuracy5 = ((float(vcorrect5) / float(vcounter5)) *100)
    if vcounter9 > 0:
        vaccuracy9 = ((float(vcorrect9) / float(vcounter9)) *100)
    else:
        vaccuracy9 = -1

    #print "net id       = " + str(vnet_id) + ", correct = " + str(vcorrect) + ",  incorrect = " + str(vincorrect) + ",  count = " + str(vcounter) + ",  accuracy = " + str(vaccuracy)
    #print "net id (0.5) = " + str(vnet_id) + ", correct = " + str(vcorrect5) + ",  incorrect = " + str(vincorrect5) + ",  count = " + str(vcounter5) + ",  accuracy = " + str(vaccuracy5)
    #print "net id (0.9) = " + str(vnet_id) + ", correct = " + str(vcorrect9) + ",  incorrect = " + str(vincorrect9) + ",  count = " + str(vcounter9) + ",  accuracy = " + str(vaccuracy9)


    sql3 = "update `network`.`network` set `training_accuracy` = "+ str(vaccuracy) + ",`TA5` = "+ str(vaccuracy5) + ",`TA9` = "+ str(vaccuracy9) + ",`no_predictions` = " + str(vcounter) + ",`no_predictions5` = "+ str(vcounter5) + ",`no_predictions9` = "+ str(vcounter9) + " where `id` = " + str(vnet_id)
    cursor3.execute(sql3)
    con.commit()
