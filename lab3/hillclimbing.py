from evolution import individual, fitness, format_individual
from pair import pair
import copy

def generateNextBestNeighbor(individual):
    bestFitness = fitness(individual)
    bestIndividual = copy.deepcopy(individual)

    size = len(individual)

    node = copy.deepcopy(individual)
    for row in range(size):
        for p in range(size):
            for i in range(1, size + 1):
                for j in range(1, size + 1):
                    node[row][p].first = i
                    node[row][p].second = j
                    
                    f = fitness(node)
                    if (f < bestFitness):
                        bestFitness = f
                        bestIndividual = copy.deepcopy(node)

            node = copy.deepcopy(individual)

    return (bestFitness, bestIndividual)



def hillClimbing(start = None):
    if start is None:
        start = individual(4)

    (curFit, curNode) = generateNextBestNeighbor(start)

    while True:
        if curFit == 0:
            return curNode

        (newFit, newNode) = generateNextBestNeighbor(curNode)

        if newFit == curFit:
            return newNode

        curFit = newFit
        curNode = newNode
    