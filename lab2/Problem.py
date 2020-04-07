
class Problem:
    def __init__(self, initial):
        self.__initialConfig = initial

    def getRoot(self):
        return self.__initialConfig


    @staticmethod
    def expand(currentConfig):
        myList = []

        for j in range(currentConfig.getSize()):
            myList.append(currentConfig.nextConfiguration(j))

        return myList

    @staticmethod
    def isSolved(board):
        # Check rows
        if board.getSize() != len(set(board.getBoard())):
            #print("Not a set")
            return False

        # No need to check columns

        # Checking Diagonals
        for x1 in range(board.getSize()):
            for x2 in range(x1 + 1, board.getSize()):
                y1 = board.getBoard()[x1]
                y2 = board.getBoard()[x2]

                slope = (y2 - y1) / (x2 - x1)
                #print("Slope of " + str(x1) + " and " + str(x2) + " = " + str(slope))

                if abs(slope) == 1.0:
                    return False
        return True
