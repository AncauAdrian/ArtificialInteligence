from utility import individual, pair, format_individual, fitness
import copy
import random

class Ant:

    def __init__(self, size): 
        self.__size = size
        self.__path = list()
        self.__fitness = None
        # Initialise the firt position of path with a random position

        self.__path.append(individual(size))
        self.evaluate()


    @property
    def path(self):
        return self.__path


    @path.setter
    def path(self, other):
        self.__path = other


    @property
    def fitness(self):
        return self.__fitness

    
    @fitness.setter
    def fitness(self, other):
        self.__fitness = other


    def evaluate(self):
s
        self.__fitness = fitness(self.__path[-1])


    def calculateMove(self, _pair, vel):
        anew = pair(_pair.first + vel.first, _pair.second + vel.second)

        if anew.first < 1 or anew.second < 1:
            return None

        if anew.first > self.__size or anew.second > self.__size:
            return None

        return anew


    def nextMoves(self, initial):
        """
        Returns a list of valid next moves starting from position initial

        initial: the initial position
        """

        size = len(initial)

        paths = []

        moves = [pair(1, 1), pair(1, 0), pair(1, -1), pair(0, 1),
                 pair(0, 0), pair(0, -1), pair(-1, 1), pair(-1, 0), pair(-1, -1)]

        node = initial.copy()
        for row in range(size):
            for p in range(size):
                for vel in moves:
                    move = copy.deepcopy(node)
                    res = self.calculateMove(node[row][p], vel)

                    if res is not None:
                        move[row][p] = res
                        paths.append(move)

        return paths


    def makeMove(self, move):
        self.__path.append(move[1])
        self.fitness = move[0]

        
    def distanceMove(self, move):
        """ Calculate distance. Bigger - better"""

        curFitness = self.fitness
        nextFitness = fitness(move)

        if(curFitness >= nextFitness):
            return curFitness - nextFitness + 2

        return 1 / (curFitness - nextFitness)

    def addMove(self, q0, trace, alpha, beta):  

        p = {}
        position = self.__path[-1]
        nextSteps = self.nextMoves(position)
        for step in nextSteps:
            p[tuple(step)]=self.distanceMove(step)

        for step in p:
            if step in trace:
                p[tuple(step)] = (p[tuple(step)] ** beta) * (trace[tuple(step)] ** alpha)
            else:
                p[tuple(step)] = (p[tuple(step)] ** beta) * ((1.0 / self.fitness) ** alpha)

        if (random.random()<q0):
            self.makeMove(sorted(p,key=lambda x:x[1],reverse=True)[0])
        else:
            value=[]
            prob=[]
            for step in p:
                value.append(step)
                prob.append(p[step])

            self.makeMove(random.choices(value,weights=prob,k=1)[0])
        return True