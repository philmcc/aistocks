#!/usr/bin/python
from pyfann import libfann

#Parameters that will be passed in
net_name = "/home/user/Documents/TrainandTestdata/ACN2.net"
train_file = "/home/user/Documents/TrainandTestdata/trainingdataFANN-ACN_out-train.dat"
test_file = "/home/user/Documents/TrainandTestdata/testdataFANN-ACN_out-train.dat"
###

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
input=test_data.get_input()
output=test_data.get_output()
for i in range(len(input)):
    #print ann.test(input[i], output[i])
    outval = ann.test(input[i], output[i])
    outval = str(outval)
    outval = outval.translate(None, '[]')

    #print output[i]
    #print "Output %f " % ann.test(input[i], output[i])
    printingstring = 'Output number ' + str(i) + ' is '+ outval
    print printingstring
print "MSE error on test data: %f" % ann.get_MSE()

ann.save(net_name)
