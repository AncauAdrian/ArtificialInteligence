from Problem import Problem
import heapq

class Controller:
    def __init__(self, problem):
        self.__problem = problem

    def rec_DFS(self, visited, current):
        # mark current board as visited
        visited.append(current)

        if Problem.isSolved(current):
            return current
        else:
            for x in Problem.expand(current):
                if x in visited:
                    return None
                else:
                    ret = self.rec_DFS(visited, x)

                    if ret is not None:
                        return ret

        return None

    def DFSrec(self, root):
        v = []

        return self.rec_DFS(v, root)

    def DFS(self, start):
        found = False
        visited = []
        toVisit = [start]  # Priority queue

        while len(toVisit) != 0 and found is False:
            if len(toVisit) == 0:
                return None

            board = toVisit.pop(0)
            visited.append(board)

            if Problem.isSolved(board) is True:
                return board
            else:
                aux = []
                for x in Problem.expand(board):
                    if x not in visited:
                        aux.append(x)

                toVisit += aux

    def greedy(self, start):
        found = False
        visited = []
        toVisit = [] # Priority queue
        heapq.heappush(toVisit, start)

        while len(toVisit) != 0 and found is False:
            if len(toVisit) == 0:
                return None

            board = heapq.heappop(toVisit)
            visited.append(board)

            if Problem.isSolved(board) is True:
                return board
            else:
                for x in Problem.expand(board):
                    if x not in visited:
                        heapq.heappush(toVisit, x)
