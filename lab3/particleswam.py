from evolution import individual, fitness as evo_fit, format_individual, population as evo_pop
from pair import pair
import copy

from random import randint, random
from operator import add

class Particle:

    def __init__(self, size):
        """
        Particle Initialiser adapted for Euler Square problem

        size: the size of the Euler square
        """

        self.__position = individual(size)
        self.evaluate()
        self.__velocity = [[pair(0,0) for i in range(size)] for i in range(size)]

        self.__bestPozition = self.__position.copy()
        self.__bestFitness = self.__fitness

    def evaluate(self):
        self.__fitness = evo_fit(self.__position)

    @property
    def fitness(self):
        ''' Fitness getter '''

        return self.__fitness

    @property
    def position(self):
        ''' Position getter '''

        return self.__position

    @property
    def velocity(self):
        ''' Velocity getter '''

        return self.__velocity

    @position.setter
    def position(self, newPosition):
        ''' Position setter, automatically calls evaluate() and replaces bestFitness and bestPosition'''

        self.__position = newPosition.copy()
        self.evaluate()

        if self.__fitness < self.__bestFitness:
            self.__bestFitness = self.__position.copy()
            self.__bestFitness = self.__fitness

    @property
    def bestPosition(self):
        return self.__bestPozition

    @bestPosition.setter
    def bestPosition(self, newBest):
        self.__bestPozition = newBest

    def __str__(self):
        return format_individual(self.__position)

    def __repr__(self):
        return self.__str__()


def population(count : int, n : int):
    ''' Creates a population of count individuals of n size '''

    return [Particle(n) for _ in range(count)]


def selectNeighbors(pop : list, nSize):
    """ Creates the neighborhood for a given population pop

    pop: population

    nSize: neighborhood size """

    if (nSize>len(pop)):
        nSize=len(pop)

    neighbors=[]
    for _ in range(len(pop)):
        localNeighbor=[]
        for _ in range(nSize):
            x = randint(0, len(pop)-1)
            while (x in localNeighbor):
                x = randint(0, len(pop)-1)
            localNeighbor.append(x)
        neighbors.append(localNeighbor.copy())
    return neighbors


def multiply(mult, par):
    return pair(par.first * mult, par.second * mult)



def iteration(pop, neighbors, c1, c2, w ):
    """
    generates an iteration

    pop: the current population
    """

    popDim = len(pop[0].position)

    bestNeighbors=[]
    for i in range(len(pop)):
        bestNeighbors.append(neighbors[i][0])

        for j in range(1, len(neighbors[i])):
            if pop[bestNeighbors[i]].fitness > pop[neighbors[i][j]].fitness:
                bestNeighbors[i] = neighbors[i][j]

    for i in range(len(pop)):
        for j in range(len(pop[0].velocity)):
            for k in range(len(pop[0].velocity[j])):
                newVelocity = multiply(w, pop[i].velocity[j][k])
                newVelocity = newVelocity + multiply(c1 * random(), (pop[bestNeighbors[i]].position[j][k] - pop[i].position[j][k])) 
                newVelocity = newVelocity + multiply(c2 * random(), (pop[i].bestPosition[j][k] - pop[i].position[j][k]))

                newVelocity.first = round(newVelocity.first)
                newVelocity.second = round(newVelocity.second)
                pop[i].velocity[j][k] = newVelocity

    for i in range(len(pop)):
        newPozition = []
        for j in range(len(pop[0].velocity)):
            newRow = []
            for k in range(len(pop[0].velocity[0])):
                res = pop[i].position[j][k] + pop[i].velocity[j][k]

                if res.first > popDim:
                    res.first = popDim

                if res.first < 1:
                    res.first = 1

                if res.second > popDim:
                    res.second = popDim

                if res.second < 1:
                    res.second = 1
                newRow.append(res)

            newPozition.append(newRow)

        pop[i].position = newPozition
    return pop


def main():
    noIteratii = 1000
    #PARAMETERS:
    
    #number of particles
    noParticles = 100
    #individual size
    dimParticle = 7

    #specific parameters for PSO
    w = 1.0
    c1 = 1.
    c2 = 2.5
    sizeOfNeighborhood = 20
    P = population(noParticles, dimParticle)

    # we establish the particles' neighbors 
    neighborhoods = selectNeighbors(P, sizeOfNeighborhood)
    
    for i in range(noIteratii):
        P = iteration(P, neighborhoods, c1, c2, w/(i+1))

    #print the best individual
    best = 0
    for i in range(1, len(P)):
        if (P[i].fitness < P[best].fitness):
            best = i
    
    fitnessOptim=P[best].fitness
    individualOptim=P[best].position
    
    print(format_individual(individualOptim))
    print(str(fitnessOptim))

    
def test():

    pop = population(10, 5)

    pop[9]

main()
    
