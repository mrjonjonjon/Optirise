from ortools.sat.python import cp_model
import json
from pprint import pprint

model = cp_model.CpModel()
solver = cp_model.CpSolver()


v1 = model.NewIntVar(0,1,f'aaaa')#[model.NewBoolVar(f'wpntype{i}') for i in range(14)]
v2 = model.NewIntVar(0,1,f'bbbb')#[model.NewBoolVar(f'wpntype{i}') for i in range(14)]
v3 = model.NewIntVar(0,100,f'cccc')#[model.NewBoolVar(f'wpntype{i}') for i in range(14)]

b = model.NewBoolVar('b')

# Implement b == (x >= 5).
model.Add(v1 == 1).OnlyEnforceIf(b)
model.Add(v1 !=1).OnlyEnforceIf(b.Not())

c = model.NewBoolVar('c')
# Implement b == (x >= 5).
model.Add(v2 == 1).OnlyEnforceIf(c)
model.Add(v2 !=1).OnlyEnforceIf(c.Not())

d = model.NewBoolVar('d')
# Implement b == (x >= 5).
model.Add(v3 == 50).OnlyEnforceIf(d)
model.Add(v3 !=50).OnlyEnforceIf(d.Not())

model.Add(d==1).OnlyEnforceIf([b,c])
model.Maximize(v1+v2)

solver.Solve(model, cp_model.VarArraySolutionPrinter([v1,v2,v3]))
