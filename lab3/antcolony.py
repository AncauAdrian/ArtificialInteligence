from evolution import individual, format_individual
from pair import pair

import copy

from random import random, choice


class Ant:
    def __init__(self, sqSize):
        """
        Creates an ant

        sqSize: size of the Euler Square
        """

        self.__size = sqSize
        self.__path = [individual(self.__size)]

    @property
    def path(self):
        return self.__path

    @path.setter
    def path(self, other):
        self.__path = other

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

    def distMove(self, a):
        dummy = Ant(self.__size)
        dummy.path = copy.deepcopy(self.__path)
        dummy.path.append(a)
        return 100 - len(dummy.nextMoves(a))

    def addMove(self, q0, trace, alpha, beta):
        # adauga o noua pozitie in solutia furnicii daca este posibil

        # pozitiile ce nu sunt valide vor fi marcate cu zero
        nextSteps = copy.deepcopy(self.nextMoves([-1]))
        # determina urmatoarele pozitii valide in nextSteps
        # daca nu avem astfel de pozitii iesim

        if (len(nextSteps) == 0):
            return False
        # punem pe pozitiile valide valoarea distantei empirice

        p = {}
        for i in nextSteps:
            p[i] = self.distMove(i)
        # calculam produsul trace^alpha si vizibilitate^beta
        p = [(p[i] ** beta) * (trace[self.path[-1]][i] ** alpha)
             for i in range(len(p))]
        if (random() < q0):
            # adaugam cea mai buna dintre mutarile posibile
            p = [[i, p[i]] for i in range(len(p))]
            p = max(p, key=lambda a: a[1])
            self.path.append(p[0])
        else:
            # adaugam cu o probabilitate un drum posibil (ruleta)
            s = sum(p)
            if (s == 0):
                return choice(nextSteps)
            p = [p[i]/s for i in range(len(p))]
            p = [sum(p[0:i+1]) for i in range(len(p))]
            r = random()
            i = 0
            while (r > p[i]):
                i = i+1
            self.path.append(i)
        return True

    def fitness(self):
        # un drum e cu atat mai bun cu cat este mai lung
        # problema de minimizare, drumul maxim e n * m
        return (self.size-len(self.path)+2)


def epoca(noAnts, n, m, trace, alpha, beta, q0, rho):
    antSet = [ant(n, m) for i in range(noAnts)]
    for i in range(n * m):
            # numarul maxim de iteratii intr-o epoca este lungimea solutiei
        for x in antSet:
            x.addMove(q0, trace, alpha, beta)
    # actualizam trace-ul cu feromonii lasati de toate furnicile
    dTrace = [1.0 / antSet[i].fitness() for i in range(len(antSet))]
    for i in range(n * m):
        for j in range(n * m):
            trace[i][j] = (1 - rho) * trace[i][j]

    for i in range(len(antSet)):
        for j in range(len(antSet[i].path)-1):
            x = antSet[i].path[j]
            y = antSet[i].path[j+1]
            trace[x][y] = trace[x][y] + dTrace[i]
    # return best ant path
    f = [[antSet[i].fitness(), i] for i in range(len(antSet))]
    f = max(f)
    return antSet[f[1]].path


def test():
    ant = Ant(4)

    print(format_individual(ant.path[0]))

    print(ant.nextMoves(ant.path[0]))


test()
