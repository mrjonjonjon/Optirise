from ortools.sat.python import cp_model



head_armor_ids=[1,2,3]
body_armor_ids = [1,2,3]
id_to_head_armor_def = {1:10,2:90,3:40}
id_to_body_armor_def = {1:50,2:10,3:10}

def solve_boolean_problem():
    # Create a CP-SAT solver
    model = cp_model.CpModel()

    

    # Create boolean variables
    id_to_head_armor_var = {id:model.NewBoolVar(f'h{id}') for id in head_armor_ids}
    id_to_body_armor_var = {id:model.NewBoolVar(f'b{id}') for id in body_armor_ids}
  


    head_armor_def_var = model.NewIntVar(0,1000,'head_def')
    body_armor_def_var = model.NewIntVar(0,1000,'body_def')


    model.Maximize(head_armor_def_var+body_armor_def_var)

    #CAN WEAR AT MOST ONE OF EACH ARMOR PIECE
    model.Add(sum(id_to_head_armor_var.values()) == 1)
    model.Add(sum(id_to_body_armor_var.values()) == 1)


    for id in head_armor_ids:
        # Define the atk value based on the selection of head[0]
        model.Add(head_armor_def_var== id_to_head_armor_def[id]).OnlyEnforceIf(id_to_head_armor_var[id])
    
    for id in body_armor_ids:
        # Define the atk value based on the selection of head[0]
        model.Add(body_armor_def_var == id_to_body_armor_def[id]).OnlyEnforceIf(id_to_body_armor_var[id])


    # Create a solver and solve the model
    solver = cp_model.CpSolver()
    status = solver.Solve(model)

    if status == cp_model.OPTIMAL or status == cp_model.FEASIBLE:
        solution = [solver.Value(body_armor_def_var),solver.Value(head_armor_def_var)]
        return solution
    else:
        return None

if __name__ == "__main__":
    solution = solve_boolean_problem()
    if solution is not None:
        print("Solution found:", solution)
    else:
        print("No solution found.")
