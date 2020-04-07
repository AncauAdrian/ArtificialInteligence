from Board import Board
from Problem import Problem
from Controller import Controller
from time import time


def tests():
    c1 = Board([0, 0, 0, 0])
    c2 = Board([0, 0, 0, 0])
    p = Problem(c1)
    contr = Controller(p)

    assert (c1 == c2)
    # Configuration
    assert (c1.getSize() == 4)
    assert (c1.getBoard() == [0, 0, 0, 0])
    print(c1.nextConfiguration(0))
    assert (c1.nextConfiguration(0).getBoard() == [1, 0, 0, 0])
    assert (c1.nextConfiguration(1).getBoard() == [0, 1, 0, 0])

    # Problem
    aux = p.expand(c1)
    assert (len(aux) == 4)
    assert (aux[0].getBoard() == [1, 0, 0, 0])

    # ...

    print('tests passed')

class UI:

    def __init__(self):
        self.__config = Board([0, 0, 0, 0])
        self.__p = Problem(self.__config)
        self.__cont = Controller(self.__p)

    def printMenu(self):
        print("N-Queens Problem")
        print("Current configuration is: n = " + str(self.__config.getSize()))
        print("0 - Exit")
        print("1 - Change Configuration")
        print("2 - DFS")
        print("3 - greedy")

    def changeConfig(self):
        self.__config = Board([0 for y in range(int(input("n = ")))])
        self.__p = Problem(self.__config)
        self.__cont = Controller(self.__p)

    def findDFS(self):
        startClock = time()
        print(str(self.__cont.DFS(self.__p.getRoot())))
        print('execution time = ', time() - startClock, " seconds")

    def findGreedy(self):
        startClock = time()
        print(str(self.__cont.greedy(self.__p.getRoot())))
        print('execution time = ', time() - startClock, " seconds")

    def run(self):
        while True:
                self.printMenu()
                command = int(input(">>"))
                if command == 0:
                    break
                elif command == 1:
                    self.changeConfig()
                elif command == 2:
                    self.findDFS()
                elif command == 3:
                    self.findGreedy()
            #except Exception as e:
                #print(e)


def main():
    tests()
    ui = UI()
    ui.run()

main()