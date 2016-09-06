#!/usr/bin/python
from pyfann import libfann
from network_functions import save_tests
from network_functions import create_net_record

# To Do
# Needs to querry Net_Group for training file name, test filename, ticker, input_nurons, output_neurons




#Parameters that will be passed in
group_id = 9

# create empty net record and get number
net_id = create_net_record(group_id)
train_file = "/home/user/Documents/TrainandTestdata/trainingdataFANN-ACN_out-train.dat"
test_file = "/home/user/Documents/TrainandTestdata/testdataFANN-ACN_out-train.dat"
ticker = "ACN"
###
# create file name as ticker_netgroup_netnumber.net
net_name = "/home/user/Documents/Networks/" + str(ticker) + "_" + str(group_id) + "_" + str(net_id) + ".net"



connection_rate = 1
learning_rate = 0.7
num_input = 7
num_neurons_hidden = 7
num_output = 1

desired_error = 0.0001
max_iterations = 1000
iterations_between_reports = 1000

ann = libfann.neural_net()
ann.create_sparse_array(connection_rate, (num_input, num_neurons_hidden, num_output))
ann.set_learning_rate(learning_rate)
ann.set_activation_function_output(libfann.SIGMOID_SYMMETRIC_STEPWISE)


train_data = libfann.training_data()
train_data.read_train_from_file(train_file)
test_data = libfann.training_data()
test_data.read_train_from_file(test_file)

ann.train_on_file(train_file, max_iterations, iterations_between_reports, desired_error)
print "\nTrain error: %f, Test error: %f\n\n" %( ann.test_data(train_data),ann.test_data(test_data))

print "Testing network again"
ann.reset_MSE()
vinput = test_data.get_input()
output = test_data.get_output()
for i in range(len(vinput)):
    outval = ann.test(vinput[i], output[i])
    outval = str(outval)
    outval = outval.translate(None, '[]')

    targetout = str(output[i])
    targetout = targetout.translate(None, '[]')


    # Store test output in net_test table as [netNumber, record(test row number), prediction, target]
    # Stillinserts into temp table net_tests2
    save_tests(net_id, i + 1, outval, targetout)
    printingstring = 'Output number ' + str(i) + ' is '+ outval + 'Should have been: ' + targetout
    print printingstring
print "MSE error on test data: %f" % ann.get_MSE()

ann.save(net_name)
