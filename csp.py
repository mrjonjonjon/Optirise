from ortools.sat.python import cp_model



head_armor_ids=[1,2,3]
body_armor_ids = [1,2,3]
head_def = {1:10,2:90,3:40}
body_def = {1:50,2:10,3:10}
def solve_boolean_problem():
    # Create a CP-SAT solver
    model = cp_model.CpModel()

    

    # Create boolean variables
    head = {id:model.NewBoolVar(f'h{id}') for id in head_armor_ids}
    body = {id:model.NewBoolVar(f'b{id}') for id in body_armor_ids}
  


    head_v = model.NewIntVar(0,1000,'head_def')
    body_v = model.NewIntVar(0,1000,'body_def')


    model.Maximize(head_v+body_v)
    #CAN WEAR AT MOST ONE OF EACH ARMOR PIECE
    model.Add(sum(head.values()) == 1)
    model.Add(sum(body.values()) == 1)


    for id in head_armor_ids:
        # Define the atk value based on the selection of head[0]
        model.Add(head_v== head_def[id]).OnlyEnforceIf(head[id])
    
    for id in body_armor_ids:
        # Define the atk value based on the selection of head[0]
        model.Add(body_v == body_def[id]).OnlyEnforceIf(body[id])


    # Create a solver and solve the model
    solver = cp_model.CpSolver()
    status = solver.Solve(model)

    if status == cp_model.OPTIMAL or status == cp_model.FEASIBLE:
        solution = [solver.Value(body_v),solver.Value(head_v)]
        return solution
    else:
        return None

if __name__ == "__main__":
    solution = solve_boolean_problem()
    if solution is not None:
        print("Solution found:", solution)
    else:
        print("No solution found.")
