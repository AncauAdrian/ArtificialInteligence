import numpy
from random import randint

class pair:
    """
    A pair of two integers
    """

    def __init__(self, first, second):
        self.__first = first
        self.__second = second

    @property
    def first(self):
        return self.__first

    @first.setter
    def first(self, first):
        self.__first = first

    @property
    def second(self):
        return self.__second

    @second.setter
    def second(self, second):
        self.__second = second

    def __str__(self):
        return "(" + str(self.__first) + ", " + str(self.__second) + ")"

    def __repr__(self):
        return self.__str__()

    def __eq__(self, value):
        return self.__first == value.first and self.__second == value.second

    def __hash__(self):
        return hash((self.__first, self.__second))

    def __add__(self, other):
        if isinstance(other, pair):
            return pair(self.first + other.first, self.second + other.second)
        return None

    def __sub__(self, other):
        if isinstance(other, pair):
            return pair(self.first - other.first, self.second - other.second)
        return None

    def __mul__(self, other):
        if isinstance(other, pair):
            return pair(self.first * other.first, self.second * other.second)

        if isinstance(other, pair):
            return pair(self.first * other, self.second * other)

        return None


def individual(n: int):
    """
    Generate a random individual

    n: the size of the Euler Matrix
    """

    return [[pair(randint(1, n), randint(1, n)) for x in range(n)] for x in range(n)]


def count_array_duplicates(array: list):
    """
    Takes in an array of pairs and counts the number of duplicates

    array: array of pairs
    """

    # The duplicates count
    count = 0

    # First elements
    firsts = []
    seconds = []

    for i in array:
        firsts.append(i.first)
        seconds.append(i.second)

    count += len(firsts) - len(set(firsts))
    count += len(seconds) - len(set(seconds))

    return count


def fitness(individual):
    """
    Determines the fitnesss of the given individual (a rating depending of how close it is to our final solution).
    0 - best, higher - worse

    individual: individual to evaluate
    """

    # Duplicates count
    count = 0

    for row in individual:
        count += count_array_duplicates(row)
        #print("row duplicates: " + str(count_array_duplicates(row)))
    
    # create numpy array of individual
    arr = numpy.array(individual)

    for i in range(len(individual)):
        count += count_array_duplicates(arr[:,i])
        #print("collumn duplicates: " + str(count_array_duplicates(arr[:,i])))

    # Transform to one dimensional array and count pair duplicates
    flattened = arr.flatten()
    count += len(flattened) - len(set(flattened))
    #print("pair duplciates: " + str(len(flattened) - len(set(flattened))))

    return count

def format_individual(individual: list):
    string = ""
    for row in individual:
        string += str(row) + '\n'

    return string