#!/usr/bin/python
from pyfann import libfann

test_data = libfann.training_data()
test_data.read_train_from_file("/home/user/Documents/TrainandTestdata/testdataFANN-ACN_out-train.dat")

ann = libfann.neural_net()
ann.create_from_file("/home/user/Documents/Pythonscripts/NN7-ACN")
