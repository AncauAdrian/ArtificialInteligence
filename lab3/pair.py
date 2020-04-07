class pair:
    """
    A pair of two integers
    """

    def __init__(self, first, second):
        self.__first = first
        self.__second = second

    @property
    def first(self):
        return self.__first

    @first.setter
    def first(self, first):
        self.__first = first

    @property
    def second(self):
        return self.__second

    @second.setter
    def second(self, second):
        self.__second = second

    def __str__(self):
        return "(" + str(self.__first) + ", " + str(self.__second) + ")"

    def __repr__(self):
        return self.__str__()

    def __eq__(self, value):
        return self.__first == value.first and self.__second == value.second

    def __hash__(self):
        return hash((self.__first, self.__second))

    def __add__(self, other):
        if isinstance(other, pair):
            return pair(self.first + other.first, self.second + other.second)
        return None

    def __sub__(self, other):
        if isinstance(other, pair):
            return pair(self.first - other.first, self.second - other.second)
        return None

    def __mul__(self, other):
        if isinstance(other, pair):
            return pair(self.first * other.first, self.second * other.second)

        if isinstance(other, pair):
            return pair(self.first * other, self.second * other)

        return None


def testPair():
    p = pair(1, 2)

    assert p.first == 1
    assert p.second == 2

    p.first = 5
    p.second = 6
    
    assert p.first == 5
    assert p.second == 6
    
    assert str(p) == "(5, 6)"

    s = pair(5, 6)
    assert p == s
    s.second = 7
    assert p != s

    p = pair(1, 2)
    s = pair(1, 2)

    test = []
    test.append(p)
    test.append(s)

    assert len(test) == 2
    assert len(set(test)) == 1

testPair()
