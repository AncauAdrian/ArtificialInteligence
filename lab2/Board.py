class Board:
    """Holds the configuration of a board"""

    def __init__(self, intial):
        self.__size = len(intial)
        self.__board = intial

    def nextConfiguration(self, position):
        if position < 0 or position >= self.__size:
            raise ValueError("Invalid position")

        ret = self.__board[:]

        if ret[position] == self.__size - 1:
            ret[position] = 0
        else:
            ret[position] += 1

        return Board(ret)

    """Gives the board a rating depending on the chance of finding a solution amongst it's configurations"""
    def heuristics(self):
        return self.__size - len(set(self.__board))

    def getSize(self):
        return self.__size

    def getBoard(self):
        return self.__board

    def __lt__(self, other):
        if not isinstance(other, Board):
            return False

        if self.heuristics() < other.heuristics():
            return True

    def __str__(self):
        _str = ""
        matrix = [[0 for y in range(self.__size)] for x in range(self.__size)]

        for i in range(self.__size):
            matrix[self.__board[i]][i] = 1

        for i in matrix:
            _str += str(i) + '\n'

        return _str

    def __eq__(self, other):
        if not isinstance(other, Board):
            return False
        if self.__size != other.getSize():
            return False
        """
        for i in range(self.__size):
            if self.__board[i] != other.getBoard()[i]:
                return False
        return True
        """
        return self.__board == other.getBoard()
