#!/usr/bin/python


def save_tests(net_id, row, prediction, target):
    import MySQLdb as mdb

    #print "SAVE Tests"
    #print "prediction"
    #print prediction

    con = None
    con = mdb.connect('localhost', 'root', 'fil1202job', 'network')
    sql_outputs = "SELECT c.no_output FROM network.network a, network.net_group b, network.net_type c where c.id = b.type and b.id = a.group and a.id = " + str(net_id)
    sql_cur = con.cursor()
    sql_cur.execute(sql_outputs)
    no_outputs = sql_cur.fetchone()

    if int(no_outputs[0]) == 1:
        #print "its 1"
        cursor = con.cursor()
        # Prepare SQL query to INSERT a record into the database.
        sql = "INSERT INTO `network`.`net_tests`(`net_id`, `row`, `prediction`,     `target`) VALUES(" + str(net_id) +"," + str(row) + "," + str(prediction)     + "," + str(target) +")"
        #net_id,row,prediction,target

        try:
            # Execute the SQL command
            cursor.execute(sql)
            # Commit your changes in the database
            con.commit()
        except:
            # Rollback in case there is any error
            con.rollback()

    else:
        #print "its 2"

        splitout = str(prediction).split(", ")
        #print splitout[0] + splitout[1]
        splittarget = str(target).split(", ")
        #print splittarget[0] + splittarget[1]
        cursor = con.cursor()
        # Prepare SQL query to INSERT a record into the database.
        sql = "INSERT INTO `network`.`net_tests`(`net_id`, `row`, `prediction`,`target`, `sell`, `target_sell`) VALUES(" + str(net_id) +"," + str(row) + "," + str(splitout[0]) + "," + str(splittarget[0]) + "," + str(splitout[1]) + "," + str(splittarget[1]) +  ")"
        print sql
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


def save_prediction(net_id, pdate, prediction):
    import MySQLdb as mdb

    #print "SAVE Prediction"

    con = None
    con = mdb.connect('localhost', 'root', 'fil1202job', 'network')

    sql_outputs = "SELECT c.no_output FROM network.network a, network.net_group b, network.net_type c where c.id = b.type and b.id = a.group and a.id = " + str(net_id)
    sql_cur = con.cursor()
    sql_cur.execute(sql_outputs)
    no_outputs = sql_cur.fetchone()

    if int(no_outputs[0]) == 1:
        #print "its 1"
        # Prepare SQL query to INSERT a record into the database.
        sql = "INSERT INTO `network`.`predictions` (`network`, `pdate`, `prediction`) VALUES(" + str(net_id) +", '" + str(pdate) + "'," + str(prediction) +")"
        #net_id,row,prediction,target
        #print sql

        try:
            # Execute the SQL command
            cursor = con.cursor()
            cursor.execute(sql)
            # Commit your changes in the database
            con.commit()
        except:
            # Rollback in case there is any error
            con.rollback()

            # disconnect from server
        con.close()
    else:
        #print "its not 1"
        #
        # Do actions for 2 output values
        #
        splitout = str(prediction).split(", ")
        #print splitout[0] + splitout[1]
        #splittarget = str(target).split(", ")
        #print splittarget[0] + splittarget[1]
        cursor = con.cursor()
        # Prepare SQL query to INSERT a record into the database.
        #sql = "INSERT INTO `network`.`net_tests`(`net_id`, `row`, `prediction`,`target`, `sell`, `target_sell`) VALUES(" + str(net_id) +"," + str(row) + "," + str(splitout[0]) + "," + str(splittarget[0]) + "," + str(splitout[1]) + "," + str(splittarget[1]) +  ")"
        sql = "INSERT INTO `network`.`predictions` (`network`, `pdate`, `prediction`, `target_sell`) VALUES(" + str(net_id) +", '" + str(pdate) + "'," + str(splitout[0]) + "," + str(splitout[1]) + ")"
        #print sql
        try:
            # Execute the SQL command
            cursor.execute(sql)
            # Commit your changes in the database
            con.commit()
        except:
            # Rollback in case there is any error
            con.rollback()


def create_net_record(group):
    net_id = ""
    import MySQLdb as mdb

    print "Creating Net Record = Group - " + str(group)
    con = None
    con = mdb.connect('localhost', 'root', 'fil1202job', 'network')

    cursor = con.cursor()
    # Prepare SQL query to INSERT a record into the database.
    sql = "INSERT INTO `network`.`network`(`group`) VALUES(" + str(group) + ")"

    # Execute the SQL command
    cursor.execute(sql)
    # Commit your changes in the database
    con.commit()

    sql = "SELECT max(id) id from network.network"

    cursor.execute(sql)
    for row in cursor.fetchall():
        net_id = row[0]
    # disconnect from server
    con.close()

    return net_id

def create_group_record(net_type, ticker):
    group_id = ""
    import MySQLdb as mdb

    print "Creating Group Record - " + str(net_type) + ", " + str(ticker)
    con = None
    con = mdb.connect('localhost', 'root', 'fil1202job', 'network')

    cursor = con.cursor()
    cursor1 = con.cursor()
    # Prepare SQL query to INSERT a record into the database.
    sql = "INSERT INTO `network`.`net_group`(type, ticker) VALUES(" + str(net_type) + ", \'" + str(ticker) + "\')"
    #print sql
    # Execute the SQL command
    cursor.execute(sql)
    # Commit your changes in the database
    con.commit()

    sql = "SELECT max(id) id from network.net_group"

    cursor1.execute(sql)

    for row1 in cursor1.fetchall():
        group_id = row1[0]
        print row1[0]
    # disconnect from server
    con.close()

    return group_id


def run_predictions():

    import MySQLdb as mdb
    from pyfann import libfann
    #from datetime import date
    from network_functions import save_prediction

    mydate = ""

    con = None
    con = mdb.connect('localhost', 'root',
            'fil1202job', 'stock');

    with con:
        cur = con.cursor(mdb.cursors.DictCursor)
        cur1 = con.cursor()
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
                print row1b
                print ann.run(row1b)
                prediction = ann.run(row1b)
                prediction = str(prediction).translate(None, '[]')
                #
                # Store results in db - Function
                #
                save_prediction(row["id"], mydate, prediction)

    calc_signals()


def create_net (group_id, num_neurons_hidden):
    from pyfann import libfann
    from network_functions import save_tests
    from network_functions import create_net_record
    import MySQLdb as mdb


    print "Create Net - " + str(group_id) + ", " + str(num_neurons_hidden)
    # To Do
    # Needs to querry Net_Group for training file name, test filename, ticker, input_nurons, output_neurons
    con = mdb.connect('localhost', 'root', 'fil1202job', 'network')
    sql = "select a.ticker, a.train_data, a.test_data, b.no_input, b.no_output from network.net_group a, network.net_type b where a.type = b.id and a.id =" + str(group_id)
    cursor = con.cursor()
    cursor.execute(sql)
    for row in cursor.fetchall():
        ticker = str(row[0])
        train_file = str(row[1])
        test_file = str(row[2])
        num_input = row[3]
        num_output = row[4]
    # disconnect from server
    #con.close()

    #Parameters that will be passed in
    #group_id = 191

    # create empty net record and get number
    net_id = create_net_record(group_id)
    print "Net ID = " + str(net_id)
    #train_file = "/home/user/Documents/TrainandTestdata/trainingdataFANN-ACN_out-train.dat"
    #test_file = "/home/user/Documents/TrainandTestdata/testdataFANN-ACN_out-train.dat"
    #ticker = "ACN"
    ###
    # create file name as ticker_netgroup_netnumber.net
    net_name = "/home/user/Documents/Networks/" + str(ticker) + "_" + str(group_id) + "_" + str(net_id) + ".net"

    sql2 = "UPDATE `network`.`network` SET `net_file` = \"" + net_name + "\" where id = " + str(net_id)
    #print sql2
    cursor2 = con.cursor()
    cursor2.execute(sql2)
    con.commit()

    connection_rate = 1
    learning_rate = 0.7
    #num_input = 7
    #num_neurons_hidden = 7
    #num_output = 1

    desired_error = 0.0001
    max_iterations = 100000
    iterations_between_reports = 10000

    ann = libfann.neural_net()
    #ann.create_sparse_array(connection_rate, (num_input, num_neurons_hidden, num_output))
    ann.create_standard_array([num_input, num_neurons_hidden, num_neurons_hidden, num_output])
    ann.set_learning_rate(learning_rate)
    ann.set_activation_function_output(libfann.SIGMOID_SYMMETRIC_STEPWISE)


    train_data = libfann.training_data()
    train_data.read_train_from_file(train_file)
    test_data = libfann.training_data()
    test_data.read_train_from_file(test_file)

    ann.train_on_file(train_file, max_iterations, iterations_between_reports, desired_error)
    print "\nTrain error: %f, Test error: %f\n\n" %( ann.test_data(train_data),ann.test_data(test_data))

    #print "Testing network again"
    ann.reset_MSE()
    vinput = test_data.get_input()
    output = test_data.get_output()
    for i in range(len(vinput)):
        #print "###"
        #print ann.test(vinput[i], output[i])
        #print "###'"
        outval = ann.test(vinput[i], output[i])
        outval = str(outval)
        outval = outval.translate(None, '[]')

        targetout = str(output[i])
        #print "###"
        #print targetout
        targetout = targetout.translate(None, '[]')
        #print targetout


        # Store test output in net_test table as [netNumber, record(test row number), prediction, target]
        # Stillinserts into temp table net_tests2
        save_tests(net_id, i + 1, outval, targetout)
        #printingstring = 'Output number ' + str(i) + ' is '+ outval + 'Should have been: ' + targetout
        #print printingstring
    #print "MSE error on test data: %f" % ann.get_MSE()

    ann.save(net_name)





def create_data_file(select, filename, inputs, outputs, rows):

    import MySQLdb as mdb

    print "Create Data File - " + str(filename) + " " + str(inputs) + " " + str(outputs) + " " + str(rows)
    #print "the select is - " + str(select)
    con = None
    con = mdb.connect('localhost', 'root', 'fil1202job', 'network')

    trainingfile = open(filename, 'wb')
    trainingfile.write(str(rows) + " " + str(inputs) + " " + str(outputs) + "\n");

    cur1 = con.cursor()
    cur1.execute(str(select))
    for row1 in cur1.fetchall():
        if outputs == 1:
            #print "Outputs -  " + str(outputs)
            outline = ""
            myout = row1[(len(row1) - 1)]
            row1b = list(row1)
            del row1b[(len(row1b) - 1)]

            for i in range(len(row1b)):
                outline = outline + str(row1b[i]) + " "
            #print outline
        elif outputs == 2:
            #print "Outputs -  " + str(outputs)
            outline = ""
            myout = row1[(len(row1) - 2)]
            myout = str(myout) + " " + str(row1[(len(row1) - 1)])
            row1b = list(row1)
            del row1b[(len(row1b) - 1)]
            del row1b[(len(row1b) - 1)]
            for i in range(len(row1b)):
                outline = outline + str(row1b[i]) + " "

        trainingfile.write(outline + "\n")
        trainingfile.write(str(myout) + "\n")
        #print "test"
    trainingfile.close();


def fill_group_record(group_id, training, testing, predict):

    import MySQLdb as mdb

    print "Filling Record Group"
    con = None
    con = mdb.connect('localhost', 'root', 'fil1202job', 'network')

    cursor = con.cursor()
    # Prepare SQL query to Update a record in the database.
    sql = "UPDATE `network`.`net_group` SET `train_data` = \"" + str(training) + "\", `test_data` = \"" + str(testing) + "\", `predict_data` = \"" + str(predict) + "\" WHERE `id` = " + str(group_id)
    #print sql
    # Execute the SQL command
    cursor.execute(sql)
    # Commit your changes in the database
    con.commit()


    # disconnect from server
    con.close()

    return group_id

def create_group(net_type, ticker):

    import MySQLdb as mdb
    from network_functions import create_group_record
    from network_functions import create_data_file
    from network_functions import fill_group_record

    #inputs
    #ticker = "ACN"
    #net_type = 1
    print "Create Group - Net Type - " + str(net_type) + " Ticker - " + ticker
    ######
    # Variables
    TrainingData_sel = ""
    TestData_sel = ""
    PredictData_sel = ""
    no_input = 0
    no_output = 0
    no_train = 0
    no_test = 0

    group_id = create_group_record(net_type, ticker)

    training_file_loc = "/home/user/Documents/TrainandTestdata/"
    training_data_out = training_file_loc + str(net_type) + "_" + str(ticker) + "_train.out"
    testing_data_out = training_file_loc + str(net_type) + "_" + str(ticker) + "_test.out"

    con = None
    con = mdb.connect('localhost', 'root', 'fil1202job', 'network')
    cursor = con.cursor()
    sql = "SELECT `net_type`.`id`, `net_type`.`TrainingData`, `net_type`.`TestData`, `net_type`.`PredictData`, `net_type`.`no_input`, `net_type`.`no_output`, `net_type`.`no_train`, `net_type`.`no_test` FROM `network`.`net_type` where id = " + str(net_type)
    cursor.execute(sql)
    for row in cursor.fetchall():
        #print row
        TrainingData_sel = str(row[1])
        TrainingData_sel = TrainingData_sel.replace("^^^TICKER^^^", ticker)
        print TrainingData_sel
        TestData_sel = str(row[2])
        TestData_sel = TestData_sel.replace("^^^TICKER^^^", ticker)
        #print TestData_sel
        PredictData_sel = str(row[3])
        PredictData_sel = PredictData_sel.replace("^^^TICKER^^^", ticker)
        #print PredictData_sel
        no_input = row[4]
        no_output = row[5]
        no_train = row[6]
        no_test = row[7]
    #
    # Create data files
    #
        create_data_file(TrainingData_sel, training_data_out, no_input, no_output, no_train)
        create_data_file(TestData_sel, testing_data_out, no_input, no_output, no_test)

    #
    # Need to  store predict data then write record to net_group
    #

        fill_group_record(group_id, training_data_out, testing_data_out, PredictData_sel)



def calc_test_accuracy():

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

        sql_outputs = "SELECT c.no_output FROM network.network a, network.net_group b, network.net_type c where c.id = b.type and b.id = a.group and a.id = " + str(vnet_id)
        sql_cur = con.cursor()
        sql_cur.execute(sql_outputs)
        no_outputs = sql_cur.fetchone()

        if int(no_outputs[0]) == 1:
            #print "Its 1"""
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

            sql1 = "SELECT prediction, target FROM network.net_tests where net_id = " + str(vnet_id)
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

            if vcounter > 0:
                vaccuracy = ((float(vcorrect) / float(vcounter)) *100)
            else:
                vaccuracy = -1
            if vcounter5 > 0:
                vaccuracy5 = ((float(vcorrect5) / float(vcounter5)) *100)
            else:
                vaccuracy5 = -1
            if vcounter9 > 0:
                vaccuracy9 = ((float(vcorrect9) / float(vcounter9)) *100)
            else:
                vaccuracy9 = -1

            #print "net id       = " + str(vnet_id) + ", correct = " + str(vcorrect) + ",  incorrect = " + str(vincorrect) + ",  count = " + str(vcounter) + ",  accuracy = " + str(vaccuracy)
            #print "net id (0.5) = " + str(vnet_id) + ", correct = " + str(vcorrect5) + ",  incorrect = " + str(vincorrect5) + ",  count = " + str(vcounter5) + ",  accuracy = " + str(vaccuracy5)
            #print "net id (0.9) = " + str(vnet_id) + ", correct = " + str(vcorrect9) + ",  incorrect = " + str(vincorrect9) + ",  count = " + str(vcounter9) + ",  accuracy = " + str(vaccuracy9)


            sql3 = "update `network`.`network` set `training_accuracy` = "+ str(vaccuracy) + ",`TA5` = "+ str(vaccuracy5) + ",`TA9` = "+ str(vaccuracy9) + ",`no_predictions` = " + str(vcounter) + ",`no_predictions5` = "+ str(vcounter5) + ",`no_predictions9` = "+ str(vcounter9) + " where `id` = " + str(vnet_id)
            cursor3.execute(sql3)

        else:
            #print "Its 2"""
            vcounter = 0
            vcorrect = 0
            #vincorrect = 0
            vaccuracy = 0
            vcounter5 = 0
            vcorrect5 = 0
            #vincorrect5 = 0
            vaccuracy5 = 0
            vcounter9 = 0
            vcorrect9 = 0
            #vincorrect9 = 0
            vaccuracy9 = 0

            sql1 = "SELECT prediction, target, sell, target_sell FROM network.net_tests where net_id = " + str(vnet_id)
            cursor1.execute(sql1)
## calc straight accuracy
            for row1 in cursor1.fetchall():
                if int(row1[1]) == 1:
                    # Should be buy
                    if float(row1[0]) > float(row1[2]):
                        vcorrect = vcorrect + 1
                elif int(row1[3]) == 1:
                    if float(row1[0]) < float(row1[2]):
                        vcorrect = vcorrect + 1
                vcounter = vcounter + 1
## Calc 0.5 accuracy
                if int(row1[1]) == 1:
                    # Should be buy
                    if float(row1[0]) > float(row1[2]):
                        if float(row1[0]) > 0.7:
                            vcorrect5 = vcorrect5 + 1
                elif int(row1[3]) == 1:
                    if float(row1[0]) < float(row1[2]):
                        if float(row1[2]) > 0.7:
                            vcorrect5 = vcorrect5 + 1
                if float(row1[0]) > 0.7 or float(row1[2]) > 0.7:
                    #print str(row1[0]) + " " + str(row1[2])
                    vcounter5 = vcounter5 + 1

## Calc 0.9 accuracy
                if int(row1[1]) == 1:
                    # Should be buy
                    if float(row1[0]) > float(row1[2]):
                        if float(row1[0]) > 0.9:
                            vcorrect9 = vcorrect9 + 1
                elif int(row1[3]) == 1:
                    if float(row1[0]) < float(row1[2]):
                        if float(row1[2]) > 0.9:
                            vcorrect9 = vcorrect9 + 1
                if float(row1[0]) > 0.9 or float(row1[2]) > 0.9:
                    #print str(row1[0]) + " " + str(row1[2])
                    vcounter9 = vcounter9 + 1


            if vcounter > 0:
                vaccuracy = ((float(vcorrect) / float(vcounter)) *100)
            else:
                vaccuracy = -1
            if vcounter5 > 0:
                vaccuracy5 = ((float(vcorrect5) / float(vcounter5)) *100)
            else:
                vaccuracy5 = -1
            if vcounter9 > 0:
                vaccuracy9 = ((float(vcorrect9) / float(vcounter9)) *100)
            else:
                vaccuracy9 = -1
            #sql3 = "update `network`.`network` set `training_accuracy` = "+ str(vaccuracy) + ",`no_predictions` = " + str(vcounter) + " where `id` = " + str(vnet_id)
            #sql3 = "update `network`.`network` set `training_accuracy` = "+ str(vaccuracy) + ",`TA5` = "+ str(vaccuracy5) + ",`no_predictions` = " + str(vcounter) + ",`no_predictions5` = "+ str(vcounter5) + " where `id` = " + str(vnet_id)
            sql3 = "update `network`.`network` set `training_accuracy` = "+ str(vaccuracy) + ",`TA5` = "+ str(vaccuracy5) + ",`TA9` = "+ str(vaccuracy9) + ",`no_predictions` = " + str(vcounter) + ",`no_predictions5` = "+ str(vcounter5) + ",`no_predictions9` = "+ str(vcounter9) + " where `id` = " + str(vnet_id)
            #print sql3
            cursor3.execute(sql3)

        con.commit()

def update_ndc():

    import MySQLdb as mdb
    from datetime import datetime

    print datetime.now()

    con = None
    con = mdb.connect('localhost', 'root', 'fil1202job', 'stock')
    cursor = con.cursor()
    sql = "SELECT id, qdate, ticker from stock.stocks where stocks.NDC is NULL;"
    cursor1 = con.cursor()
    cursor.execute(sql)
    for row in cursor.fetchall():
        #print sql
        sql2 = "select stocks.close from stock.stocks where stocks.qdate > \"" + str(row[1]) + "\" and ticker = \"" + str(row[2]) + "\" order by qdate asc limit 1"
        cursor2 = con.cursor()
        cursor2.execute(sql2)
        for row2 in cursor2.fetchall():
            sql3 = "update stock.stocks set stocks.NDC = " + str(row2[0]) + "where id = " + str(row[0])
            cursor3 = con.cursor()
            cursor3.execute(sql3)

    con.commit()
    con.close()
    print datetime.now()

def update_stock_data():
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
    sql = "select distinct(ticker) from stock.tickers"
    vsdate =  "20130301"

    cur.execute(sql)
    tickers = cur.fetchall()
    count=0
    for ticker in tickers:
        if count < 10000:
            sql2 = "select ifnull(date_format(max(qdate),'%Y%m%d'),'20040601') from stock.stocks where ticker = \"" + str(ticker[0]) + "\""
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
                    sql3 = "INSERT INTO `stock`.`stocks` (`ticker`,`qdate`,`open`,`high`,`low`,`close`,`volume`) VALUES(\"" + str(ticker[0]) + "\", \"" + quote[0] + "\", " + quote[1] + ", " + quote[2] + ", " + quote[3] + ", " + quote[4] + ", " + quote[5] + ")"
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

    update_ndc()


def calc_signals():

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

        sql2 = "update network.predictions set signal5 = " + str(signal5) + ", signal8 = " + str(signal8) + ", signal9 = " + str(signal9) + " where id = " + str(prediction[0])
        cur2.execute(sql2)
    con.commit()
    con.close()

def update_indecies_data():

    import ystockquote
    import MySQLdb as mdb
    import datetime

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
