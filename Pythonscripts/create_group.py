#!/usr/bin/python

import MySQLdb as mdb
from network_functions import create_group_record
from network_functions import create_data_file
from network_functions import fill_group_record

#inputs
ticker = "ACN"
net_type = 2

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
    TrainingData_sel = row[1]
    TrainingData_sel = TrainingData_sel.replace("^^^TICKER^^^", ticker)
    #print TrainingData_sel
    TestData_sel = row[2]
    TestData_sel = TestData_sel.replace("^^^TICKER^^^", ticker)
    #print TestData_sel
    PredictData_sel = row[3]
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
