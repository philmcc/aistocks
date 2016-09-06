#!/usr/bin/python
from pyfann import libfann

desired_error = 0.0001
max_iterations = 10000
iterations_between_reports = 1000

ann = libfann.neural_net()
ann.create_from_file("/home/user/Documents/TrainandTestdata/NN7-ACN.net")
ann.train_on_file("/home/user/Documents/TrainandTestdata/trainingdataFANN-ACN_out-train.dat", max_iterations, iterations_between_reports, desired_error)

