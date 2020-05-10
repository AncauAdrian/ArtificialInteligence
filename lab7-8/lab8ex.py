import copy
from typing import Tuple

import matplotlib.pyplot as pyplot
import numpy as np

FILE_LENGTH = 0
LEARNING_RATE = 0.00001


def training_data_test_ratio():
    return FILE_LENGTH * 4 // 5


def test_data_training_ratio():
    return FILE_LENGTH - training_data_test_ratio()


class NPArrays:
    
    def __init__(self, X, Y):
        self.X = X
        self.Y = Y


def read_data() -> NPArrays:
    """
    Reads the data from the file and saves it into a dataclass containing two np.ndarrays
    """
    global FILE_LENGTH
    X, Y = [], []
    with open('in.csv', 'r') as input_file:
        for line in input_file:
            split_line = line.split(',')
            X += [[1, *split_line[:-1]]]
            Y += [split_line[-1]]
            FILE_LENGTH += 1
    return NPArrays(np.asarray(X, dtype=np.float),
                    np.asarray(Y, dtype=np.float)
                    .reshape(-1, 1))  # Transforms Y into a column vector


def split_into_training_and_test(dataset: NPArrays) -> Tuple[NPArrays, NPArrays]:
    """
    Splits a NPArrays data into training and test data
    """
    return (
        NPArrays(
                copy.deepcopy(dataset.X[:training_data_test_ratio()]),
                copy.deepcopy(dataset.Y[:training_data_test_ratio()])
                ),
        NPArrays(
                copy.deepcopy(dataset.X[training_data_test_ratio():]),
                copy.deepcopy(dataset.Y[training_data_test_ratio():])
                )
        )


def activation_function(x: np.ndarray or list) -> np.ndarray or list:
    """
    The activation function for the ANN. In this case, it is the identity function f(x) = x
    """
    return x


def activation_derivative_function(_) -> float:
    """
    The derivative of the activation function for the ANN. In this case, it is f(x) = 1
    """
    return 1.0


class ArtificialNeuralNetwork:
    def __init__(self, dataset: NPArrays, hidden_layer_neurons: int):
        self.input_layer = dataset.X
        self.expected_output = dataset.Y
        self.hidden_layer_neurons = hidden_layer_neurons
        self.length = self.input_layer.shape[0]
        self.width = self.input_layer.shape[1]

        # We create all of the weights with a random value between 0 and 1 initially
        self.weights = [np.asarray(np.random.rand(self.width, self.hidden_layer_neurons)),
                        np.asarray(np.random.rand(self.hidden_layer_neurons, 1))]
        self.layer1 = None
        self.output_layer = None
        self.loss = []

    def feed_forward(self) -> None:
        """
        Take the values from the input layer, and pass them through the algorithm
        :return:
        """
        self.layer1 = activation_function(np.dot(self.input_layer, self.weights[0]))
        self.output_layer = activation_function(np.dot(self.layer1, self.weights[1]))

    def compute_value(self, row: np.ndarray) -> np.ndarray:
        """
        Pass a set of value to the input layer, pass them through the algorithm and return the
            output layer's final value
        """
        layer_1 = activation_function(np.dot(row, self.weights[0]))
        output = activation_function(np.dot(layer_1, self.weights[1]))
        return output

    def back_propagation(self, learning_rate):
        """
        Change the weights based on how far off they were from the expected result
        """
        # Calculate the amount by which weights should be changed
        output_error = 2 * (self.expected_output - self.output_layer)
        activation_derivative = activation_derivative_function(self.output_layer)
        hidden_1_derivative = activation_derivative_function(self.layer1)

        weights_delta_0 = np.asarray(
                np.dot(self.input_layer.T,
                       np.dot(output_error * activation_derivative,
                              self.weights[1].T) * hidden_1_derivative))
        weights_delta_1 = np.asarray(
                np.dot(self.layer1.T, (output_error * activation_derivative)))

        # Update the old weights
        self.weights[0] += (1 / self.length) * learning_rate * weights_delta_0
        self.weights[1] += (1 / self.length) * learning_rate * weights_delta_1

        # Add the loss so it can be graphed at the end
        self.loss.append(sum((self.expected_output - self.output_layer) ** 2))


if __name__ == '__main__':
    full_dataset = read_data()
    training_data, test_data = split_into_training_and_test(full_dataset)
    ann = ArtificialNeuralNetwork(training_data, 32)

    # Run the algorithm for each training data
    for i in range(training_data_test_ratio()):
        ann.feed_forward()
        ann.back_propagation(LEARNING_RATE)
        ann.input_layer = copy.deepcopy(training_data.X)
        ann.expected_output = copy.deepcopy(training_data.Y)

    pyplot.plot(list(range(training_data_test_ratio())), ann.loss)
    pyplot.xlabel('Iterations')
    pyplot.ylabel('Loss Value')
    pyplot.title('Loss Value by Iteration for Training Data')
    pyplot.legend()
    pyplot.show()

    # Print Expected vs Actual values, calculate Average Loss
    loss = 0
    for i in range(len(test_data.X)):
        computed_value = ann.compute_value(test_data.X[i])[0]
        print(f'Expected {test_data.Y[i][0]}, Actual {computed_value}')
        loss += abs((test_data.Y[i][0] - computed_value))

    print('-' * 50)
    print(f'Average loss (error): {loss / test_data_training_ratio():.5f}')