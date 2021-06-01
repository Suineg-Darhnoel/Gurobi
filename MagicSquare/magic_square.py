import gurobipy as gp
from gurobipy import GRB

n = 3

# Create Model
ms_model = gp.Model("Magic_Square_{0}x{0}".format(n))

# Add variables
ms_vars = ms_model.addVars(n, n, n**2, vtype=GRB.BINARY, name="X")
S = ms_model.addVar(vtype=GRB.INTEGER, name="S")

ms_model.update()
# Set objective function
# -- no objective function
ms_model.setObjective(1)

# Add constraints
# All cell must be used only once
celldiff_constr = ms_model.addConstrs(
            (ms_vars.sum('*', '*', v) == 1
                for v in range(n**2)),
            name="cell_diff"
        )

# Row Sum = S
rowsum_constr = ms_model.addConstrs(
            (gp.quicksum((v+1)*ms_vars.sum(i, '*', v)
                for v in range(n**2)) == S
                for i in range(n)),
            name="row_sum"
        )

# Col Sum = S
colsum_constr = ms_model.addConstrs(
            (gp.quicksum((v+1)*ms_vars.sum('*', i, v)
                for v in range(n**2)) == S
                for i in range(n)),
            name="col_sum"
        )

# DiagonalSum = S
diagsum_constr = ms_model.addConstr(
            gp.quicksum((v+1)*ms_vars[i, i, v]
                for i in range(n)
                for v in range(n**2)) == S,
            name="diag_sum"
        )

# Anti-DiagonalSum = S
anti_diagsum_constr = ms_model.addConstr(
            gp.quicksum((v+1)*ms_vars[n-i-1, i, v]
                for i in range(n)
                for v in range(n**2)) == S,
            name="anti_diag_sum"
        )

# write model to a file
ms_model.write("magic_square.lp")

# Solve the model
# ms_model.setParam("PoolSearchMode", 2)
# ms_model.setParam("PoolSolutions", 10)
ms_model.optimize()

# for i in range(10):
#     ms_model.setParam("SolutionNumber", i)
#     ms_model.printAttr("Xn")

# Write solution to a file
try:
    ms_model.write("magic_square.sol")
except gp.GurobiError as e:
    print("Error: ", e)
