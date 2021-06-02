#!/usr/bin/python3

"""
This program aims to solve kakkuro
using IP with the help of gurobipy library
"""

import gurobipy as gp # library for integer programming
import numpy as np # for convinience
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
        [1, 1, 1, 1, 1],
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

# -- Add Variables
# Create variables for every blank cell
cell_vars = kmodel.addVars(
            row_num,
            col_num,
            pattern_num,
            vtype=GRB.BINARY,
            name='X'
        ) # [checked]

# CONSTRAINTS
# Cell Constraints
# -- One of the values [1-9] must be taken
cell_constr = kmodel.addConstrs(
            (cell_vars.sum(x, y+i, '*') == 1
                for x in range(row_num)
                for y in range(col_num)
                for i in range(coord2range(hhints, (x, y)))
                if b[x, y+i] == 1),
            name="CELL"
        ) # [checked]

# Add Horizontal Constraints
# -- No redundant values in the same horizontal block
h_constr = kmodel.addConstrs(
            (cell_vars[i, j1, v]+cell_vars[i, j2, v] <= 1
                for i in range(row_num)
                for j1 in range(col_num)
                for j2 in range(col_num)
                for v in range(pattern_num)
                if b[i, j1] == 1 and b[i, j2] == 1 and [i, j1] != [i, j2])
        )

# -- Each sum of the consecutive hcells is equal to the given value
hsum_constr = kmodel.addConstrs(
            (gp.quicksum((v+1)*cell_vars[x, y+i, v]
                for v in range(pattern_num)
                for i in range(coord2range(hhints, (x, y)))
                if b[x, y+i] == 1) == coord2val(hhints, (x, y))

                for x in range(row_num)
                for y in range(col_num)
                if coord2val(hhints, (x, y)) != 0
            ),
            name="H_SUM"
        ) # [checked]

# Add Vertical Constraints
# -- No redundant values in the same vertical block
v_constr = kmodel.addConstrs(
            (cell_vars[i1, j, v]+cell_vars[i2, j, v] <= 1
                for i1 in range(row_num)
                for i2 in range(row_num)
                for j in range(col_num)
                for v in range(pattern_num)
                if b[i1, j] == 1 and b[i2, j] == 1 and [i1, j] != [i2, j])
        )
# -- Each sum of the consecutive vcells is equal to the given value
vsum_constr = kmodel.addConstrs(
            (gp.quicksum((v+1)*cell_vars[x+i, y, v]
                for v in range(pattern_num)
                for i in range(coord2range(vhints, (x, y)))
                if b[x+i, y] == 1) == coord2val(vhints, (x, y))

                for x in range(row_num)
                for y in range(col_num)
                if coord2val(vhints, (x, y)) != 0
            ),
            name="V_SUM"
        ) # [checked]

# Set no objective function
kmodel.setObjective(0)

# Optimize
kmodel.optimize()

# Print Solutions
import re
# print(kmodel.printAttr('x'))

for v in kmodel.getVars():
    value = v.getAttr(GRB.Attr.X)
    name  = v.getAttr(GRB.Attr.VarName)
    row, col, ans = re.findall('[0-9]+', name)
    if value == 1:
        print("({}, {}) = {}".format(row, col, int(ans)+1))

# Write a solution to a file
try:
    kmodel.write("kakkuro.sol")
except gp.GurobiError as e:
    print("Error: ", e)

# Write model to a file
kmodel.write('kakkuro.lp')
