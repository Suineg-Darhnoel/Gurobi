## Setting up Gurobi on Linux Environment

1. How to install Gurobi

- Go to Gurobi download website (https://www.gurobi.com/downloads/)
- Unpack the package, then install with

~~~shell
python setup install
~~~

2. Get your license

- Register your name to get your license
- Activate your license with `grbgetkey` command which can be found in the download package

~~~shell
grbgetkey *your license key*
~~~

3. Install Jupyter-notebook

~~~shell
pip install jupyter
~~~

If you encounter Jupyter Notebook's "500 : Internal Server Error", try to do this

~~~shell
pip install --upgrade jupyterhub
pip install --upgrade --user nbconvert
~~~

## Test Gurobi with Python's API

Source code can be found at https://www.gurobi.com/documentation/9.1/examples/matrix2_py.html

~~~python
#!/usr/bin/env python3.7

# Copyright 2021, Gurobi Optimization, LLC

# This example uses the Python matrix API to formulate the n-queens
# problem; it maximizes the number queens placed on an n x n
# chessboard without threatening each other.
#
# This example demonstrates NumPy slicing.

import numpy as np
import scipy.sparse as sp
import gurobipy as gp
from gurobipy import GRB


# Size of the n x n chess board
n = 8

try:
    # Create a new model
    m = gp.Model("matrix2")

    # Create a 2-D array of binary variables
    # x[i,j]=1 means that a queen is placed at square (i,j)
    x = m.addMVar((n, n), vtype=GRB.BINARY, name="x")

    # Set objective - maximize number of queens
    m.setObjective(x.sum(), GRB.MAXIMIZE)

    # Add row and column constraints
    for i in range(n):

        # At most one queen per row
        m.addConstr(x[i, :].sum() <= 1, name="row"+str(i))

        # At most one queen per column
        m.addConstr(x[:, i].sum() <= 1, name="col"+str(i))

    # Add diagonal constraints
    for i in range(1, 2*n):

        # At most one queen per diagonal
        diagn = (range(max(0, i-n), min(n, i)), range(min(n, i)-1, max(0, i-n)-1, -1))
        m.addConstr(x[diagn].sum() <= 1, name="diag"+str(i))

        # At most one queen per anti-diagonal
        adiagn = (range(max(0, i-n), min(n, i)), range(max(0, n-i), min(n, 2*n-i)))
        m.addConstr(x[adiagn].sum() <= 1, name="adiag"+str(i))

    # Optimize model
    m.optimize()

    print(x.X)
    print('Queens placed: %g' % m.objVal)

except gp.GurobiError as e:
    print('Error code ' + str(e.errno) + ": " + str(e))

except AttributeError:
    print('Encountered an attribute error')
~~~

1. Name the source file : `matrix2.py`

2. Run command

   ~~~
   python matrix2.py
   ~~~

   Result should be :

   ~~~shell
   Academic license - for non-commercial use only - expires 2021-07-28
   Using license file /home/linak/gurobi.lic
   Gurobi Optimizer version 9.1.2 build v9.1.2rc0 (linux64)
   Thread count: 6 physical cores, 12 logical processors, using up to 12 threads
   Optimize a model with 46 rows, 64 columns and 256 nonzeros
   Model fingerprint: 0x189a5c49
   Variable types: 0 continuous, 64 integer (64 binary)
   Coefficient statistics:
     Matrix range     [1e+00, 1e+00]
     Objective range  [1e+00, 1e+00]
     Bounds range     [1e+00, 1e+00]
     RHS range        [1e+00, 1e+00]
   Found heuristic solution: objective 5.0000000
   Presolve removed 4 rows and 0 columns
   Presolve time: 0.00s
   Presolved: 42 rows, 64 columns, 269 nonzeros
   Variable types: 0 continuous, 64 integer (64 binary)
   
   Root relaxation: objective 8.000000e+00, 33 iterations, 0.00 seconds
   
       Nodes    |    Current Node    |     Objective Bounds      |     Work
    Expl Unexpl |  Obj  Depth IntInf | Incumbent    BestBd   Gap | It/Node Time
   
   H    0     0                       8.0000000   64.00000   700%     -    0s
        0     0          -    0         8.00000    8.00000  0.00%     -    0s
   
   Explored 0 nodes (66 simplex iterations) in 0.00 seconds
   Thread count was 12 (of 12 available processors)
   
   Solution count 2: 8 5
   
   Optimal solution found (tolerance 1.00e-04)
   Best objective 8.000000000000e+00, best bound 8.000000000000e+00, gap 0.0000%
   [[0. 0. 0. 0. 1. 0. 0. 0.]
    [0. 1. 0. 0. 0. 0. 0. 0.]
    [0. 0. 0. 0. 0. 0. 0. 1.]
    [1. 0. 0. 0. 0. 0. 0. 0.]
    [0. 0. 0. 1. 0. 0. 0. 0.]
    [0. 0. 0. 0. 0. 0. 1. 0.]
    [0. 0. 1. 0. 0. 0. 0. 0.]
    [0. 0. 0. 0. 0. 1. 0. 0.]]
   Queens placed: 8
   ~~~

   