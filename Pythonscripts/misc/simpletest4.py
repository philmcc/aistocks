#!/usr/bin/python
from pyfann import libfann

#Parameters that will be passed in
net_name = "/home/user/Documents/TrainandTestdata/ACN2.net"
train_file = "/home/user/Documents/TrainandTestdata/trainingdataFANN-ACN_out-train.dat"
test_file = "/home/user/Documents/TrainandTestdata/testdataFANN-ACN_out-train.dat"
###


num_neurons_hidden = 7


desired_error = 0.0001
max_iterations = 1000
iterations_between_reports = 1000

train_data = libfann.training_data()
train_data.read_train_from_file(train_file)
test_data = libfann.training_data()
test_data.read_train_from_file(test_file)

ann = libfann.neural_net()
ann.create_shortcut_array([len(train_data.get_input()[0]), len(train_data.get_output()[0])])

# Params for Cascade
desired_error = 0.0001
max_neurons = 40
neurons_between_reports = 1
steepnesses = [0.1,0.2,0.4,0.5,0.6,0.7,0.8,0.9,1.0,1.1]



# SET UP Cascade Training
ann.set_training_algorithm(libfann.TRAIN_RPROP);

ann.set_activation_function_hidden(libfann.SIGMOID_SYMMETRIC);
ann.set_activation_function_output(libfann.LINEAR_PIECE);
ann.set_activation_steepness_hidden(0.5);
ann.set_activation_steepness_output(0.5);

ann.set_train_error_function(libfann.ERRORFUNC_LINEAR);

ann.set_rprop_increase_factor(1.2);
ann.set_rprop_decrease_factor(0.5);
ann.set_rprop_delta_min(0.0);
ann.set_rprop_delta_max(50.0);

ann.set_cascade_output_change_fraction(0.01);
ann.set_cascade_output_stagnation_epochs(12);
ann.set_cascade_candidate_change_fraction(0.01);
ann.set_cascade_candidate_stagnation_epochs(12);
ann.set_cascade_weight_multiplier(0.4);
ann.set_cascade_candidate_limit(1000.0);
ann.set_cascade_max_out_epochs(150);
ann.set_cascade_max_cand_epochs(150);
ann.set_cascade_activation_steepnesses(steepnesses);
ann.set_cascade_num_candidate_groups(1);


ann.print_parameters();


ann.cascadetrain_on_data(train_data, max_neurons, neurons_between_reports, desired_error);

ann.print_connections();


print "\nTrain error: %f, Test error: %f\n\n" %( ann.test_data(train_data),ann.test_data(test_data))

#ann.train_on_data(train_data, max_iterations, iterations_between_reports, desired_error)
ann.save(net_name)