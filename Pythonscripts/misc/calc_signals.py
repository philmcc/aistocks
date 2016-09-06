#!/usr/bin/python

    import MySQLdb as mdb

    con = None
    con = mdb.connect('localhost', 'root','fil1202job', 'stock');
    cur = con.cursor()
    cur2 = con.cursor()
    sql = "select id, prediction from network.predictions"
    cur.execute(sql)
    predictions = cur.fetchall()
    for prediction in predictions:
        signal5 = 0
        signal8 = 0
        signal9 = 0
        if prediction[1] > 0.5:
            signal5 = 1
        if prediction[1] > 0.8:
            signal8 = 1
        if prediction[1] > 0.9:
            signal9 = 1
        if prediction[1] < -0.5:
            signal5 = -1
        if prediction[1] < -0.8:
            signal8 = -1
        if prediction[1] < -0.9:
            signal9 = -1

        sql2 = "update network.predictions set signal5 = " + str(signal5) + ", signal8 = " + str(signal8) + ", signal9 = " + str(signal9) + " where id = " + prediction[0]
        cur2.execute(sql2)
    con.commit()
    con.close()
