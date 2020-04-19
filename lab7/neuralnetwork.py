"""
Neural netowrk for solving the following problem:

We have a dataset containing rows of 6 columns

X1      X2      X3      X4      X5      ExpectedValue
47.88   8.39    49.29   6.31    -37.27  304.84

Find a, b, c, d such that:
a * X1 + b * X2 + c * X3 + d * x4 + X5 ~= ExpectedValue (approximates as closely)

"""


import numpy as np


#the activation function:
def sigmoid(x):
    return 1.0 / (1 + np.exp(-x))

#the derivate of te activation function
def sigmoid_derivative(x):
    return x * (1.0 - x)

class NeuralNetwork:

    def __init__(self, input: list):
        """ 
        Constructor for a NeuralNetwork class

        Input: a list that consists of a row of inputs (including the expected value)
        """

        self.introduce_data(input)


    def introduce_data(self, input: list):
        self.__inputLayer = input[0:4]
        self.__expectedValue  = input[5]


