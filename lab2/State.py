from Board import Board


class State:
    """
    holds a PATH of boards
    """

    def __init__(self):
        self.__values = []

    def setValues(self, values):
        self.__values = values[:]

    def getValues(self):
        return self.__values[:]

    def __str__(self):
        s = ''
        for x in self.__values:
            s += str(x) + "\n"
        return s

    def __add__(self, something):
        aux = State()
        if isinstance(something, State):
            aux.setValues(self.__values + something.getValues())
        elif isinstance(something, Board):
            aux.setValues(self.__values + [something])
        else:
            aux.setValues(self.__values)
        return aux
