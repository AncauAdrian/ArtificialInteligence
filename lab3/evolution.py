"""
This is an evolutionary algorithm that finds Euler matrixes that have a given condition

Process:
1. Genereates an initial population
2. Combine elements of the population with a slight chance of mutation
3. Sort the elements of the population depending on how close they are to the solution
4. Natural selection: select the best part of the population to carry on to the next
5. Repeat from step 2


Final solution should look like

1,1 | 2,3 | 3,2
----|-----|----
2,2 | 3,1 | 1,3
----|-----|----
3,3 | 1,2 | 2,1

"""


from random import randint, random
from pair import pair
import numpy
import copy


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

def population(count: int, n: int):
    """
    Creates a population with a given number of individuals

    count: the number of individuals in the population

    n: the size of the individual
    """

    pop = []
    for _ in range(count):
        x = individual(n)
        
        pop.append([fitness(x), x])

    return sorted(pop, key= lambda x: x[0])


def mutate(individual, probability: float):
    """
    Performs a mutation on an individual if successful

    individual: the individual to perform the mutation on
    probability: the probability that the mutation is successfull
    """

    if probability > random():
        positionx = randint(0, len(individual) - 1)
        positiony = randint(0, len(individual) - 1)
        first = randint(1, len(individual))
        second = randint(1, len(individual))

        individual[positionx][positiony] = pair(first, second)
    
    return individual

        
def crossover(parent1, parent2):
    """
    Crosses two parents and produces a child
    """

    child = copy.deepcopy(parent1)

    for i in range(len(parent2)):
        if(random() > 0.5):
            child[i] = copy.deepcopy(parent2[i])

    return child


def iteration(pop: list, prob: float, reprate: float):
    """
    Perform an iteration of the population

    pop: the current population

    prob: the mutation probability

    reprate: the rate at witch the population reproduces, ex: 1/3 only the top 3rd of the
    population reproduces
    """
    i1 = randint(0, int(len(pop) - 1 * reprate))
    i2 = randint(0, int(len(pop) - 1 * reprate))
    if i1 != i2:
        c = crossover(pop[i1][1], pop[i2][1])
        c = mutate(c, prob)

        fc = fitness(c)
        
        # Compare with the worst individual and replace it if better
        if fc <= pop[len(pop) - 1][0]:
            pop[len(pop) - 1] = [fc, c]
            pop.sort(key = lambda x: x[0])
    return pop

def format_individual(individual: list):
    string = ""
    for row in individual:
        string += str(row) + '\n'

    return string
        

def evolutionary(noIterations, individualsize, popsize, probability, reprate, signal, fsignal):
    p = population(popsize, 4)

    cur = p[0]
    for _ in range(noIterations):
        p = iteration(p, probability, reprate)

        if cur != p[0]:
            cur = p[0]

        signal.emit(format_individual(cur[1]), cur[0])

    graded = sorted(p, key = lambda x: x[0])
    
    best = graded[0]
    ind = best[1]
    fitness = best[0]

    signal.emit(format_individual(ind), fitness)
    fsignal.emit("Finished")



def test():
    i = [[pair(1, 1) for x in range(5)] for x in range(5)]

    print(format_individual(i))

    print(str(fitness(i)))

test()