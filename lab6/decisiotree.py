import pandas as pd
from question import Question
from tree import *
from utility import *


def partition(rows, question):
    """Partitions a dataset"""

    true_rows, false_rows = [], []
    for row in rows:
        if question.match(row):
            true_rows.append(row)
        else:
            false_rows.append(row)
    return true_rows, false_rows


def find_best_split(rows):
    """Find the best question to ask"""

    best_gain = 0
    best_question = None
    current_uncertainty = gini(rows)

    for col in range(1, len(rows[0])): 
        values = unique_vals(rows, col) 

        for val in values:

            question = Question(col, val)
            true_rows, false_rows = partition(rows, question)

            if len(true_rows) == 0 or len(false_rows) == 0:
                continue

            gain = info_gain(true_rows, false_rows, current_uncertainty)

            if gain >= best_gain:
                best_gain, best_question = gain, question

    return best_gain, best_question


def build_tree(rows):
    """Builds the tree"""

    gain, question = find_best_split(rows)

    if gain == 0:
        return Leaf(rows)

    true_rows, false_rows = partition(rows, question)

    true_branch = build_tree(true_rows)
    false_branch = build_tree(false_rows)

    return Node(question, true_branch, false_branch)


def classify(row, node):
    """See the 'rules of recursion' above."""

    if isinstance(node, Leaf):
        return node.predictions

    if node.question.match(row):
        return classify(row, node.true_branch)
    else:
        return classify(row, node.false_branch)


def importdata(): 
    balance_data = pd.read_csv('balance-scale.data', sep= ',', header = None) 
      
    return balance_data.values

""" 
def statistics(data, tree):
    for row in data:
        correctclass = row[0]
        prediction = print_leaf(classify(row, tree))
        print("Class: %s   Prediction: %s" % (correctclass, prediction))
"""

def statistics(data, tree):
    correct_predictions = 0
    for row in data:
        correctclass = row[0]
        prediction = list(classify(row, tree).keys())[0]
        if correctclass == prediction:
            correct_predictions += 1
            print("Class: %s   Prediction: %s (correct)" % (correctclass, prediction))
        else:
            print("Class: %s   Prediction: %s (wrong)" % (correctclass, prediction))

    print("Correct predictions: " + str(correct_predictions) + " out of " + str(len(data)))
    print("Accuracy: " + str(correct_predictions / len(data) * 100.0) + "%")


def main():
    data = importdata()
    train_size = .45

    train_data = []

    for i in range(int(len(data) * train_size)):
        train_data.append(data[i])

    tree = build_tree(train_data)
    #print_tree(tree, "")

    statistics(data, tree)



if __name__ == "__main__":
    main()