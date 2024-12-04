# -*- coding: utf-8 -*-
"""
Created on Fri Nov 22 23:13:18 2024

@author: Admin
"""
# Call gurobipy library
import gurobipy as gp
from gurobipy import *

# Call pandas library
import pandas as pd

# Sets
I = 5 # Set of source (San Diego, ..., Portland)
J = 3 # Set of destination (Seattle, ..., Kansas City)

# Parameters
transport_cost = [
  [5,7,8],
  [10,8,6],
  [9,4,3],
  [12,6,2],
  [4,10,11]
]

open_cost = [0,0,350000,200000,480000]

demand = [3000,8000,9000]

supply = [2500,2500,10000,10000,10000]

# Create model
model = gp.Model('Transport')

# Create variables x = model.addVars(*indices, lb=0.0, ub=None, obj=0.0, vtype=GRB.CONTINUOUS, name="")
x = model.addVars(I, J, lb=0, vtype=GRB.CONTINUOUS, name = 'quantity shipped from i to j')
y = model.addVars(I, vtype = GRB.BINARY, name = 'open or not')

# Set objective function model.setObjective(expression, sense)
objective = gp.quicksum(transport_cost[i][j]*x[i,j] for i in range(I) for j in range(J)) + gp.quicksum(open_cost[i]*y[i] for i in range(I))
model.setObjective(objective,GRB.MINIMIZE)

# Constraints
model.addConstrs((gp.quicksum(x[i,j] for j in range(J)) <= y[i]*supply[i] for i in range(I)), name = 'supply constraint')
model.addConstrs((gp.quicksum(x[i,j] for i in range(I)) >= demand[j] for j in range(J)), name = 'demand constraint')

# Optimize model
model.optimize()
