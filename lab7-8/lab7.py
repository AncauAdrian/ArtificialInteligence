import copy
from dataclasses import dataclass
from typing import List, Tuple

import numpy as np

FILE_LENGTH = 0

training_data_test_ratio = lambda n: n * 4 // 5


@dataclass
class NPArrays:
    X: np.ndarray
    Y: np.ndarray


def read_data() -> NPArrays:
    global FILE_LENGTH
    X, Y = [], []
    with open('../input_file.csv', 'r') as input_file:
        for line in input_file:
            split_line = line.split(',')
            X += [[1, *split_line[:-1]]]
            Y += [split_line[-1]]
            FILE_LENGTH += 1
    return NPArrays(np.asarray(X, dtype=np.float),
                    np.asarray(Y, dtype=np.float)
                    .reshape(-1, 1))  # Transforms Y into a column vector


def split_into_training_and_test(dataset: NPArrays) -> Tuple[NPArrays, NPArrays]:
    return (
        NPArrays(
                copy.deepcopy(dataset.X[:training_data_test_ratio(FILE_LENGTH)]),
                copy.deepcopy(dataset.Y[:training_data_test_ratio(FILE_LENGTH)])
                ),
        NPArrays(
                copy.deepcopy(dataset.X[training_data_test_ratio(FILE_LENGTH):]),
                copy.deepcopy(dataset.Y[training_data_test_ratio(FILE_LENGTH):])
                )
        )


def least_squares_multiple_regression(dataset: NPArrays) -> np.ndarray:
    """
    Applies the formula W = (X_transpose * X)^-1 * X_transpose * Y
    This obtains the matrix of weights
    """
    X_transpose = dataset.X.transpose()
    X_transpose_times_X = np.matmul(X_transpose, dataset.X)
    inverse = np.linalg.inv(X_transpose_times_X)
    inverse_times_X_transpose = np.matmul(inverse, X_transpose)
    weights_ = np.matmul(inverse_times_X_transpose, dataset.Y)
    return weights_


def calculate_loss(dataset: NPArrays, weights_: np.ndarray) -> Tuple[List[List[float]], float]:
    def calculate_loss_for_row(dataset_line: np.ndarray, result: np.ndarray,
                               weights__: np.ndarray) -> list:
        """
        Calculates the squared loss for one row of the array
        Returns a list with 3 fields, as follows:
            Predicted_Result   Actual_Result   Loss
        """
        predicted = np.ndarray.item(
                sum(val * weight for val, weight in zip(dataset_line, weights__)))
        actual = np.ndarray.item(result)

        # We use the squared loss rather than an absolute value for better accuracy
        row_loss = (actual - predicted) ** 2
        return [predicted, actual, row_loss]

    results_ = []
    for i in range(dataset.X.shape[0]):
        results_ += [calculate_loss_for_row(dataset.X[i], dataset.Y[i], weights_)]
    return (
        [x[:-1] for x in results_],
        sum(x[-1] for x in results_)
        )


if __name__ == '__main__':
    full_dataset = read_data()
    training_data, test_data = split_into_training_and_test(full_dataset)
    weights = least_squares_multiple_regression(training_data)
    results, loss = calculate_loss(test_data, weights)
    for result_row in results:
        print(f'Expected {result_row[0]}, Actual {result_row[1]}')
    print('-' * 50)
    print(f'Total squared loss (error): {loss:.5f}')