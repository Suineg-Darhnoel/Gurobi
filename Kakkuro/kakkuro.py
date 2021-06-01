import gurobipy as gp
import numpy as np
from gurobipy import GRB

# THIS PROGRAM AIMS TO SOLVE KAKKURO
# BY INTEGER PROGRAMMING USING GUROBIPY

# Blank and Occupied cells
b = np.array([
        [0, 1, 1, 0, 0],
        [0, 1, 1, 1, 1],
        [1, 1, 0, 1, 1],
        [1, 1, 1, 1, 1],
        [0, 0, 1, 1, 0]
    ])

# Given Hints
# -- Horizonal Hints
hhints = np.array([
            {(0, 1):(3, 2)},
            {(1, 0):(16, 5)},
            {(2, 0):(3, 2)},
            {(2, 3):(13, 2)},
            {(3, 0):(17, 5)},
            {(4, 2):(16, 2)}
        ])

# -- Vertical Hints
vhints = np.array([
            {(1, 0):(7, 3)},
            {(0, 1):(10, 4)},
            {(0, 2):(4, 2)},
            {(3, 2):(9, 2)},
            {(1, 3):(30, 4)},
            {(1, 4):(8, 3)}
        ])

# Show Hypothesis
# print(b)
# print(hhints)
# print(vhints)

# -- Create Model

kmodel = gp.Model("kakkuro")

# -- Add Variables
# Create variables for every blank cell


