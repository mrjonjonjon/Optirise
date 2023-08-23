from ortools.sat.python import cp_model

import json
with open("json/armor.json", "r") as json_file:
    json_armor_data = json_file.read()

with open("json/types.json", "r") as json_file:
    json_deco_data = json_file.read()

armor_data = json.loads(json_armor_data)
deco_data = json.loads(json_deco_data)

print('DATA PARSED')
def h(a):
    ans=0
    for i in range(4):
        ans+=a[i]*(i+1)
    return ans


model = cp_model.CpModel()



# Create boolean ARMOR variables
id_to_head_armor_var = {id:model.NewBoolVar(f'h{id}') for id in range(0,len(armor_data['helm']))}
id_to_body_armor_var = {id:model.NewBoolVar(f'c{id}') for id in range(0,len(armor_data['chest']))}
id_to_arm_armor_var = {id:model.NewBoolVar(f'a{id}') for id in range(0,len(armor_data['arm']))}
id_to_waist_armor_var = {id:model.NewBoolVar(f'w{id}') for id in range(0,len(armor_data['waist']))}
id_to_leg_armor_var = {id:model.NewBoolVar(f'l{id}') for id in range(0,len(armor_data['leg']))}


#CREATE INTEGER DECO VARIABLES
deco_name_to_dist_vars={}
for level in range(4):
    for pair in deco_data['decoLevels'][level]:
        name=list(pair.keys())[0]
        deco_name_to_dist_vars[f'{name}_{level+1}']={ part:model.NewIntVar(0,3,f'{name}_{level+1}_{part}') for part in ['helm','chest','arm','waist','leg']}
                    
#DEFENSE VARIABLES
head_armor_def_var = model.NewIntVar(0,1000,'head_def')
body_armor_def_var = model.NewIntVar(0,1000,'body_def')
arm_armor_def_var = model.NewIntVar(0,1000,'arm_def')
waist_armor_def_var = model.NewIntVar(0,1000,'waist_def')
leg_armor_def_var = model.NewIntVar(0,1000,'leg_def')

#DECO SLOT VARIABLES
head_deco_slots_vars = [model.NewIntVar(0,3,f'hdeco{i}') for i in range(4)]#number of slots of each level
body_deco_slots_vars = [model.NewIntVar(0,3,f'bdeco{i}') for i in range(4)]
arm_deco_slots_vars = [model.NewIntVar(0,3,f'adeco{i}') for i in range(4)]
waist_deco_slots_vars = [model.NewIntVar(0,3,f'wdeco{i}') for i in range(4)]
leg_deco_slots_vars = [model.NewIntVar(0,3,f'ldeco{i}') for i in range(4)]



#==============CONTRAINTS==============================
#SET OBJECTIVE
#model.Minimize(deco_name_to_dist_vars[f'WirebugWhisperer_2']['helm'])
model.Maximize((deco_name_to_dist_vars['AmmoUp_3']['leg']))

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

#DECOS CANT EXCEED SLOTS

for level in range(4):  
    #decos can go in higher level slots
    model.Add(sum(deco_name_to_dist_vars[f'{list(pair.keys())[0]}_{u_level+1}']['helm'] for pair in deco_data['decoLevels'][level] for u_level in range(level,4) if f'{list(pair.keys())[0]}_{u_level+1}' in deco_name_to_dist_vars)<=sum(head_deco_slots_vars[u_level] for u_level in range(level,4)))
    model.Add(sum(deco_name_to_dist_vars[f'{list(pair.keys())[0]}_{u_level+1}']['chest'] for pair in deco_data['decoLevels'][level] for u_level in range(level,4) if f'{list(pair.keys())[0]}_{u_level+1}' in deco_name_to_dist_vars)<=sum(body_deco_slots_vars[u_level] for u_level in range(level,4)))
    model.Add(sum(deco_name_to_dist_vars[f'{list(pair.keys())[0]}_{u_level+1}']['arm'] for pair in deco_data['decoLevels'][level] for u_level in range(level,4) if f'{list(pair.keys())[0]}_{u_level+1}' in deco_name_to_dist_vars)<=sum(arm_deco_slots_vars[u_level] for u_level in range(level,4)))
    model.Add(sum(deco_name_to_dist_vars[f'{list(pair.keys())[0]}_{u_level+1}']['waist'] for pair in deco_data['decoLevels'][level] for u_level in range(level,4) if f'{list(pair.keys())[0]}_{u_level+1}' in deco_name_to_dist_vars)<=sum(waist_deco_slots_vars[u_level] for u_level in range(level,4)))
    model.Add(sum(deco_name_to_dist_vars[f'{list(pair.keys())[0]}_{u_level+1}']['leg'] for pair in deco_data['decoLevels'][level] for u_level in range(level,4) if f'{list(pair.keys())[0]}_{u_level+1}' in deco_name_to_dist_vars)<=sum(leg_deco_slots_vars[u_level] for u_level in range(level,4)))

    #num decos is at most num slots
    #model.Add(sum(deco_name_to_dist_vars[f'{list(pair.keys())[0]}_{level+1}']['helm'] for pair in deco_data['decoLevels'][level] if f'{list(pair.keys())[0]}_{level+1}' in deco_name_to_dist_vars)<=sum(head_deco_slots_vars))





    #model.Add(sum(deco_name_to_dist_vars[f'{list(pair.keys())[0]}_{level+1}']['chest'] for pair in deco_data['decoLevels'][level])<=body_deco_slots_vars[level])
    #model.Add(sum(deco_name_to_dist_vars[f'{list(pair.keys())[0]}_{level+1}']['arm'] for pair in deco_data['decoLevels'][level])<=arm_deco_slots_vars[level])
    #model.Add(sum(deco_name_to_dist_vars[f'{list(pair.keys())[0]}_{level+1}']['waist'] for pair in deco_data['decoLevels'][level])<=waist_deco_slots_vars[level])
    #model.Add(sum(deco_name_to_dist_vars[f'{list(pair.keys())[0]}_{level+1}']['leg'] for pair in deco_data['decoLevels'][level])<=leg_deco_slots_vars[level])


        






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
        model.Add(waist_deco_slots_vars[i]==armor_data['waist'][id]['decos'][i]).OnlyEnforceIf(id_to_waist_armor_var[id])

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

    print("Solution found:", solution)
    print(solver.Value(deco_name_to_dist_vars['AffinitySliding_1']['helm']))

