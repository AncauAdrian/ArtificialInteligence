# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""


import matplotlib.pyplot as plt
import numpy as np

def distribution():
    print("Select a distribution: ")
    print("1. Normal")
    print("2. Gamma")
    n = int(input("Selection = "))
    
    lower = int(input("LowerBound = "))
    upper = int(input("UpperBound = "))
    
    mu = (lower + upper) / 2
    sigma = (upper - mu) / 4
    
    if n == 1:
        dist = np.random.normal(mu, sigma, 100)
    elif n == 2:
        dist = np.random.gamma(mu, sigma, 100)
    00
    
    plt.plot(dist, 'ro')
    plt.show()
    
def allUnique(x):
    seen = set()
    return not any(i in seen or seen.add(i) for i in x)

def check_sudoku(puzzle):
    for i in range(4):
        #print(puzzle[i, :])
        if allUnique(puzzle[i, :]) is False:
            return False
        
    for i in range(4):
        #print(puzzle[:, i])
        if allUnique(puzzle[:, i]) is False:
            return False
        
            
    block_size = 2
    size = 4
    for i in range(size):
        block_row, block_column = divmod(i, block_size)
        block = puzzle[block_row*block_size:(block_row+1)*block_size, block_column*block_size:(block_column+1)*block_size]
        #print(block)
        if not allUnique(block.reshape(size)):
            return False
        
    return True

def refactor(board, original):
    for i in range(4):
        for j in range(4):
            if original[i,j] != 0:
                board[i,j] = original[i,j]

def solve_sudoku(max_attempts):
    puzzle = np.array([[3, 0, 0, 2],
                       [0, 1, 4, 0],
                       [1, 2, 0, 4],
                       [0, 3, 2, 1]])
    
    print("Max number of trials: " + str(max_attempts))
    print("Checking combinations...")
    
    #tes = np.array([[2, 3, 1, 4], [4, 1, 3, 2], [3, 4, 2, 1], [1, 2, 4, 3]])

    res = False
    while max_attempts != 0 and res == False:
        r = np.random.randint(low=1, high=5, size=(4, 4))
        refactor(r, puzzle)
        res = check_sudoku(r)
        max_attempts -= 1
        
    if res == True:
        print("Solution found!")
        print(r)
    else:
        print("No solution has been found")


print("Select a problem: ")
print("1. Sudoku")
print("2. Cryptarithmetic game")
print("3. Geometric forms")
print("4. Distribution")

choice = int(input("Selection = "))

if choice != 4:
    max_attempts = int(input("Max Attempts = "))
    
if choice == 4:
    distribution()
elif choice == 1:
    solve_sudoku(max_attempts)
    
    