"""
Neural netowrk for solving the following problem:

We have a dataset containing rows of 6 columns

X1      X2      X3      X4      X5      ExpectedValue
47.88   8.39    49.29   6.31    -37.27  304.84

Solve
a * X1 + b * X2 + c * X3 + d * x4 + X5 ~= ExpectedValue (approximates as closely)

"""
import matplotlib.pyplot as pyplot
import numpy as np


# the activation function:
def sigmoid(x):
    return 1.0 / (1 + np.exp(-x))

def sigmoid_derivative(x):
    return x * (1.0 - x)

def linear(x):
    a = 1
    b = 0
    return x * a + b

def linear_derivative():
    return 1.0


def read_data():
    data = []
    file = open('in.csv', 'r')
    lines = file.readlines()

    for line in lines:
        x = []
        split = line.split(",")
        for el in split:
            x.append(float(el))

        data.append(x)

    file.close()
    return data
    

class NeuralNetwork:

    def __init__(self, hidden_size : int):
        """ 
        Constructor for a NeuralNetwork class

        Input: a list that consists of a row of inputs (including the expected value)
        """

        # size of the hidden layer
        self.__hiddenSize = hidden_size

        self.generate_weights()
        self.loss = []


    def introduce_data(self, input_normal: list):
        input = np.array(input_normal)
        self.__inputLayer = np.asarray([input[0:5]])
        self.__expectedValue  = input[5]
        self.__hiddenLayer = None


    def generate_weights(self):
        """ Generate random weights """
        self.__weightsI2H = np.random.rand(5, self.__hiddenSize)
        self.__weightsH2O = np.random.rand(self.__hiddenSize, 1)


    def feed_forward(self):
        """ Computes the ouput of the network for current input and weights """
        
        # L(x) = L(X-1) X Weights(L(X-1)) where X is the dot produt
        self.__hiddenLayer = linear(np.dot(self.__inputLayer, self.__weightsI2H))
        self.__outputLayer = linear(np.dot(self.__hiddenLayer, self.__weightsH2O))

        return self.__outputLayer[0][0], self.__expectedValue

    
    def backprop(self, l_rate):
        """
        Change the weights based on how far off they were from the expected result
        """
        
        # the derivative of the error function
        error_deriv = np.asarray(2 * (self.__expectedValue - self.__outputLayer))

        # calculate the delta of the weights from hidden to output
        d_weightsH2O = np.dot(self.__hiddenLayer.T, (error_deriv * linear_derivative()))

        # calculate the delta of the weights from input to hiddden
        d_weightsI2H = np.dot(self.__inputLayer.T, 
        (np.dot(error_deriv * linear_derivative(), self.__weightsH2O.T) * linear_derivative()))

        self.__weightsI2H += l_rate * d_weightsI2H
        self.__weightsH2O += l_rate * d_weightsH2O
        self.loss.append(((self.__expectedValue - self.__outputLayer)**2)[0][0])

        #print("Result: " + str(self.__outputLayer[0][0]) + " --- Expected: " + str(self.__expectedValue))
    

def train(n : NeuralNetwork, train_data, l_rate):
    for d in train_data:
        n.introduce_data(d)
        for i in range(1, 7):
            n.feed_forward()
            n.backprop(l_rate / i)


def main():
    data = read_data()
    l_rate = 0.00002
    n = NeuralNetwork(15)
    
    train(n, data[0:int(len(data) * .8)], l_rate)
    pyplot.plot(range(len(n.loss)), n.loss, scalex=True)
    pyplot.xlabel('Iterations')
    pyplot.ylabel('Loss Value')
    pyplot.title('Loss Value by Iteration for Training Data')
    pyplot.legend()
    pyplot.show()

    for d in data[int(len(data) * .8) : len(data)]:
        n.introduce_data(d)
        res, expected = n.feed_forward()
        print("Result: " + str(res) + "  ---   Expected: " + str(expected))

if __name__ == "__main__":
    main()


