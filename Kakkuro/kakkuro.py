#!/usr/bin/python3

# THIS PROGRAM AIMS TO SOLVE KAKKURO
# BY INTEGER PROGRAMMING USING GUROBIPY

import gurobipy as gp
import numpy as np
from gurobipy import GRB


# UTIL FUNCTIONS
# decode coordinate to value
def coord2val(hints, coord):
    try:
        return hints[coord][0]
    except KeyError:
        return 0

# decode coordinate to range
def coord2range(hints, coord):
    try:
        return hints[coord][1]
    except KeyError:
        return 0

# function test
def test():
    print(coord2val(hhints, (0, 1)) == 3)
    print(coord2range(hhints, (0, 1)) == 2)
    print(coord2val(hhints, (1, 0)) == 16)
    print(coord2range(hhints, (1, 0)) == 5)

# Data Structures

# Blank(1) and Occupied(0) cells
b = np.array([
        [0, 1, 1, 0, 0],
        [0, 1, 1, 1, 1],
        [1, 1, 0, 1, 1],
        [1, 1, 1, 1, 1],
        [0, 0, 1, 1, 0]
    ])

# Given Hints
# -- Horizonal Hints
"""
key: the coordinate of the first blank cell
item:
  - value of summation,
  - number of consecutive cells
  (in right-to-left direction)
"""
hhints = {
            (0, 1):(3, 2),
            (1, 0):(16, 5),
            (2, 0):(3, 2),
            (2, 3):(13, 2),
            (3, 0):(17, 5),
            (4, 2):(16, 2)
         }

# -- Vertical Hints
"""
key: the coordinate of the first blank cell
item:
  - value of summation,
  - number of consecutive cells
    (in top down direction)
"""
vhints = {
            (1, 0):(7, 3),
            (0, 1):(10, 4),
            (0, 2):(4, 2),
            (3, 2):(9, 2),
            (1, 3):(30, 4),
            (1, 4):(8, 3)
         }

# test()
# Preliminary
# Dimension
row_num, col_num = b.shape
pattern_num = 9 # [1-9]

# -- Create Model
kmodel = gp.Model("kakkuro")

# Set no objective function
kmodel.setObjective(0)

# -- Add Variables
# Create variables for every blank cell
cell_vars = kmodel.addVars(
            row_num,
            col_num,
            pattern_num,
            vtype=GRB.BINARY,
            name='X'
        )

# Add constraints for unused variables (Occupied cell)
occupied_vars_constr = kmodel.addConstrs(
            (cell_vars[i, j, k] == 0
                for i in range(row_num)
                for j in range(col_num)
                for k in range(pattern_num)
                if b[i, j] == 0
            ),
            name="OV"
        )

# CONSTRAINTS

# Add Horizontal Constraints
# -- No redundant numbers in the consecutive cells
h_constr = kmodel.addConstrs(
            (cell_vars.sum(x, y+i, '*') == 1
                for x in range(row_num)
                for y in range(col_num)
                for i in range(coord2range(hhints, (x, y)))),
            name="H"
        )

# -- Each sum of the consecutive cells is equal to the given value
hsum_constr = kmodel.addConstrs(
            (gp.quicksum((v+1)*cell_vars.sum(x, y+i, v)
                for v in range(pattern_num)) == coord2val(hhints, (x, y))
                for x in range(row_num)
                for y in range(col_num)
                for i in range(coord2val(hhints, (x, y)))
                # if b[x, y] == 1
            ),
            name="H_SUM"
        )

# Add Vertical Constraints
v_constr = kmodel.addConstrs(
            (cell_vars.sum(x+i, y, '*') == 1
                for x in range(row_num)
                for y in range(col_num)
                for i in range(coord2range(vhints, (x, y)))),
            name="V"
        )

vsum_constr = kmodel.addConstrs(
            (gp.quicksum((v+1)*cell_vars.sum(x, y+i, v)
                for v in range(pattern_num)) == coord2val(vhints, (x, y))
                for x in range(row_num)
                for y in range(col_num)
                for i in range(coord2val(vhints, (x, y)))
                # if b[x, y] == 1
            ),
            name="V_SUM"
        )

# Optimize
kmodel.optimize()

# Write model to a file
kmodel.write('kakkuro.lp')
