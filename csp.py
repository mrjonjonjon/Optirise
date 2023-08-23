from ortools.sat.python import cp_model

import json
with open("json/armor.json", "r") as json_file:
    json_data = json_file.read()


armor_data = json.loads(json_data)

print('DATA PARSED')

def solve_boolean_problem():
    model = cp_model.CpModel()

    

    # Create boolean ARMOR variables
    id_to_head_armor_var = {id:model.NewBoolVar(f'h{id}') for id in range(0,len(armor_data['helm']))}
    id_to_body_armor_var = {id:model.NewBoolVar(f'c{id}') for id in range(0,len(armor_data['chest']))}
    id_to_arm_armor_var = {id:model.NewBoolVar(f'a{id}') for id in range(0,len(armor_data['arm']))}
    id_to_waist_armor_var = {id:model.NewBoolVar(f'w{id}') for id in range(0,len(armor_data['waist']))}
    id_to_leg_armor_var = {id:model.NewBoolVar(f'l{id}') for id in range(0,len(armor_data['leg']))}

    #CREATE INTEGER DECO VARIABLES
    #id_to_deco_var={id:model.NewIntVar(0,5,f'deco_{id}') for id in range()}
  

    #DEFENSE VARIABLES
    head_armor_def_var = model.NewIntVar(0,1000,'head_def')
    body_armor_def_var = model.NewIntVar(0,1000,'body_def')
    arm_armor_def_var = model.NewIntVar(0,1000,'arm_def')
    waist_armor_def_var = model.NewIntVar(0,1000,'waist_def')
    leg_armor_def_var = model.NewIntVar(0,1000,'leg_def')

    head_deco_slots_vars = [model.NewIntVar(0,3,f'hdeco{i}') for i in range(4)]#number of slots of each level
    body_deco_slots_vars = [model.NewIntVar(0,3,f'bdeco{i}') for i in range(4)]
    arm_deco_slots_vars = [model.NewIntVar(0,3,f'adeco{i}') for i in range(4)]
    waist_deco_slots_vars = [model.NewIntVar(0,3,f'wdeco{i}') for i in range(4)]
    leg_deco_slots_vars = [model.NewIntVar(0,3,f'ldeco{i}') for i in range(4)]



    #SET OBJECTIVE
    model.Maximize(-head_armor_def_var-body_armor_def_var-arm_armor_def_var-waist_armor_def_var-leg_armor_def_var)

    #CAN WEAR AT MOST ONE OF EACH ARMOR PIECE
    model.Add(sum(id_to_head_armor_var.values()) == 1)
    model.Add(sum(id_to_body_armor_var.values()) == 1)
    model.Add(sum(id_to_arm_armor_var.values()) == 1)
    model.Add(sum(id_to_waist_armor_var.values()) == 1)
    model.Add(sum(id_to_leg_armor_var.values()) == 1)

    #NO LAYERED ARMORS
    model.Add(head_armor_def_var!=0)
    model.Add(body_armor_def_var!=0)
    model.Add(arm_armor_def_var!=0)
    model.Add(waist_armor_def_var!=0)
    model.Add(leg_armor_def_var!=0)

    #MAPPING ARMOR VARIABLES TO THEIR PROPERTIES
    for id in range(0,len(armor_data['helm'])):
        model.Add(head_armor_def_var == armor_data['helm'][id]['def']).OnlyEnforceIf(id_to_head_armor_var[id])
        for i in range(4):
            model.Add(head_deco_slots_vars[i]==armor_data['helm'][id]['decos'][i]).OnlyEnforceIf(id_to_head_armor_var[id])
    
    for id in range(0,len(armor_data['chest'])):
        model.Add(body_armor_def_var == armor_data['chest'][id]['def']).OnlyEnforceIf(id_to_body_armor_var[id])
        for i in range(4):
            model.Add(body_deco_slots_vars[i]==armor_data['chest'][id]['decos'][i]).OnlyEnforceIf(id_to_body_armor_var[id])

    for id in range(0,len(armor_data['arm'])):
        model.Add(arm_armor_def_var == armor_data['arm'][id]['def']).OnlyEnforceIf(id_to_arm_armor_var[id])
        for i in range(4):
            model.Add(arm_deco_slots_vars[i]==armor_data['arm'][id]['decos'][i]).OnlyEnforceIf(id_to_arm_armor_var[id])

    for id in range(0,len(armor_data['waist'])):
        model.Add(waist_armor_def_var == armor_data['waist'][id]['def']).OnlyEnforceIf(id_to_waist_armor_var[id])
        for i in range(4):
            model.Add(waist_deco_slots_vars[i]==armor_data['waist'][id]['decos'][i]).OnlyEnforceIf(id_to_head_armor_var[id])

    for id in range(0,len(armor_data['leg'])):
        model.Add(leg_armor_def_var == armor_data['leg'][id]['def']).OnlyEnforceIf(id_to_leg_armor_var[id])
        for i in range(4):
            model.Add(leg_deco_slots_vars[i]==armor_data['leg'][id]['decos'][i]).OnlyEnforceIf(id_to_leg_armor_var[id])

    #MAPPING DECO VARIABLES


    # Create a solver and solve the model
    solver = cp_model.CpSolver()
    status = solver.Solve(model)



    #PRINT THE SOLUTION

    if status == cp_model.OPTIMAL or status == cp_model.FEASIBLE:
        selected_head_armor_id = None
        selected_body_armor_id = None
        selected_arm_armor_id= None
        selected_waist_armor_id = None 
        selected_leg_armor_id = None

        for id, var in id_to_head_armor_var.items():
            if solver.BooleanValue(var):
                selected_head_armor_id = id
                break

        for id, var in id_to_body_armor_var.items():
            if solver.BooleanValue(var):
                selected_body_armor_id = id
                break
        for id, var in id_to_arm_armor_var.items():
            if solver.BooleanValue(var):
                selected_arm_armor_id = id
                break
        
        for id, var in id_to_waist_armor_var.items():
            if solver.BooleanValue(var):
                selected_waist_armor_id = id
                break

        for id, var in id_to_leg_armor_var.items():
            if solver.BooleanValue(var):
                selected_leg_armor_id = id
                break

        solution = {
            'selected_head_armor': armor_data['helm'][selected_head_armor_id]['name'],
            'selected_body_armor': armor_data['chest'][selected_body_armor_id]['name'],
            'selected_arm_armor': armor_data['arm'][selected_arm_armor_id]['name'],
            'selected_waist_armor': armor_data['waist'][selected_waist_armor_id]['name'],
            'selected_leg_armor': armor_data['leg'][selected_leg_armor_id]['name'],
        }

        return solution

if __name__ == "__main__":
    solution = solve_boolean_problem()
    if solution is not None:
        print("Solution found:", solution)
    else:
        print("No solution found.")
