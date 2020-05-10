from utility import class_counts


class Node:
    """A Decision Node asks a question.

    This holds a reference to the question, and to the two child nodes.
    """

    def __init__(self, question, true_branch, false_branch):
        self.question = question
        self.true_branch = true_branch
        self.false_branch = false_branch


class Leaf:
    """A Leaf node classifies data """

    def __init__(self, rows):
        self.predictions = class_counts(rows)


def print_tree(node, spacing=""):
    """Pretty prints a tree"""


    if isinstance(node, Leaf):
        print (spacing + "Predict", node.predictions)
        return
        
    print (spacing + str(node.question))

    print (spacing + '--> True:')
    print_tree(node.true_branch, spacing + "  ")

    print (spacing + '--> False:')
    print_tree(node.false_branch, spacing + "  ")


def print_leaf(counts):
    """A nicer way to print the predictions at a leaf."""
    total = sum(counts.values()) * 1.0
    probs = {}
    for lbl in counts.keys():
        probs[lbl] = str(int(counts[lbl] / total * 100)) + "%"
    return probs