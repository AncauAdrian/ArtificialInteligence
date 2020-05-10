class Question:
    """ A Question is used to partition a dataset """

    def __init__(self, column, value):
        self.column = column
        self.value = value

    def match(self, example):

        val = example[self.column]
        
        return val >= self.value
    def __repr__(self):

        return "Is %s >= %s?" % (
            self.column, str(self.value))

'''
class Question:
    """ A Question is used to partition a dataset """

    possibleOps = ["==", ">=", "<="]

    def __init__(self, column, value, operation):
        """ operation: ==, >=, <= """
        self.column = column
        self.value = value
        self.operation = operation

    def match(self, example):
        val = example[self.column]

        if self.operation == "==":
            return val == self.value

        if self.operation == ">=":
           return val >= self.value

        if self.operation == "<=":
            return val <= self.value

    def __repr__(self):

        return "Is %s %s %s?" % (
            self.column, self.operation, str(self.value))

'''