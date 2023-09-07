from ortools.sat.python import cp_model
import json
from pprint import pprint
import multiprocessing
import random
from utils import sharded_range,sharded_range_for,distribute_decos,my_pretty_print
class VarArraySolutionPrinter(cp_model.CpSolverSolutionCallback):
    def __init__(self, variables,max_solutions=1):
        cp_model.CpSolverSolutionCallback.__init__(self)
        self.__variables = variables
        self.__solution_count = 0
        self.__max_solutions = max_solutions

        self.printed_solution_count=0
        self.armor_sets_decos=set()

    def on_solution_callback(self):
        self.__solution_count += 1
    
        #if self.__solution_count>100:self.StopSearch()
        id_to_head_armor_var=self.__variables['id_to_head_armor_var']
        id_to_body_armor_var=self.__variables['id_to_body_armor_var']
        id_to_arm_armor_var=self.__variables['id_to_arm_armor_var']
        id_to_waist_armor_var=self.__variables['id_to_waist_armor_var']
        id_to_leg_armor_var=self.__variables['id_to_leg_armor_var']
        armor_data=self.__variables['armor_data']
        deco_name_dist_vars=self.__variables['deco_name_to_dist_vars']
        deco_data=self.__variables['deco_data']
        weapon_type_vars = self.__variables['weapon_type_vars']
        id_to_weapon_var = self.__variables['id_to_weapon_var']
        id_to_weapon_type = self.__variables['id_to_weapon_type']
        weapon_data=self.__variables['weapon_data']


        selected_body_armor_id = None
        selected_arm_armor_id = None
        selected_helm_armor_id=None
        selected_waist_armor_id=None
        selected_leg_armor_id=None
        
        selected_weapon_type_id=None
        selected_weapon_id=None

        for id, var in id_to_body_armor_var.items():
            if self.BooleanValue(var):
                selected_body_armor_id = id
                break

        for id, var in id_to_head_armor_var.items():
            if self.BooleanValue(var):
                selected_helm_armor_id = id
                break

        for id, var in id_to_arm_armor_var.items():
            if self.BooleanValue(var):
                selected_arm_armor_id = id
                break

        for id, var in id_to_waist_armor_var.items():
            if self.BooleanValue(var):
                selected_waist_armor_id = id
                break

        for id, var in id_to_leg_armor_var.items():
            if self.BooleanValue(var):
                selected_leg_armor_id = id
                break

        for id,var in weapon_type_vars.items():
            if self.BooleanValue(var):
                selected_weapon_type_id= id
                break

        for id,var in id_to_weapon_var.items():
            if self.BooleanValue(var):
                selected_weapon_id= id
                break


        selected_deco_names=[]
        for name,var in deco_name_dist_vars.items():
            for _ in range((self.Value(var))):
                selected_deco_names.append(name)

        deco_dist=distribute_decos(selected_deco_names=selected_deco_names,\
                                   selected_helm_armor_id=selected_helm_armor_id,\
                                    selected_body_armor_id=selected_body_armor_id,\
                                    selected_arm_armor_id=selected_arm_armor_id,\
                                    selected_waist_armor_id=selected_waist_armor_id,\
                                    selected_leg_armor_id=selected_leg_armor_id,\
                                    armor_data=armor_data,\
                                    deco_data=deco_data,
                                    selected_weapon_type_id=selected_weapon_type_id,
                                    selected_weapon_id= selected_weapon_id,
                                    weapon_data=weapon_data,
                                    id_to_weapon_type=id_to_weapon_type)

        helm_name=armor_data['helm'][selected_helm_armor_id]['name']
        chest_name=armor_data['chest'][selected_body_armor_id]['name']
        arm_name=armor_data['arm'][selected_arm_armor_id]['name']
        waist_name=armor_data['waist'][selected_waist_armor_id]['name']
        leg_name=armor_data['leg'][selected_leg_armor_id]['name']

        #if (helm_name,chest_name,arm_name,waist_name,leg_name) in self.armor_sets_decos:return

        self.printed_solution_count+=1
       # weapon_type = id_to_weapon_type[selected_weapon_type_id]
        #weapon_name = eval(f'{weapon_type}_data["weapons"][{selected_weapon_id}]["weapon"]')

        solution = {
            'weapon':weapon_data[id_to_weapon_type[selected_weapon_type_id]]['weapons'][selected_weapon_id]['weapon'],
            'weapon_decos':deco_dist['weapon'],
            'helm':armor_data['helm'][selected_helm_armor_id]['name'],
            'helm_decos':deco_dist['helm'],
            'chest':armor_data['chest'][selected_body_armor_id]['name'],
            'chest_decos':deco_dist['body'],
            'arm':armor_data['arm'][selected_arm_armor_id]['name'],
            'arm_decos':deco_dist['arm'],
            'waist':armor_data['waist'][selected_waist_armor_id]['name'],
            'waist_decos':deco_dist['waist'],
            'leg':armor_data['leg'][selected_leg_armor_id]['name'],
            'leg_decos':deco_dist['leg'],
        
        }        
        my_pretty_print(solution)
        print('\n\n')
        #TODO:SINCE THIS IS MULTIPROCESSED, MUST DIVIDE BY 32. USE A PIPE OR SOMETHING
        if self.__solution_count >= self.__max_solutions:
            print(f"Stopped search after {self.__max_solutions} solutions")
            self.StopSearch()




    def solution_count(self):
        return self.__solution_count
    


def get_solutions(shard_index,num_shards):
    #print(f'process {shard_index} started')
    #OPENING/LOADING JSONS
    with open("json/armor.json", "r") as json_file:
        json_armor_data = json_file.read()
    with open("json/types.json", "r") as json_file:
        json_deco_data = json_file.read()
    with open("json/Bow.json", "r") as json_file:
        json_bow_data = json_file.read()
    with open("json/ChargeBlade.json", "r") as json_file:
        json_chargeblade_data = json_file.read()
    with open("json/DualBlades.json", "r") as json_file:
        json_dualblades_data = json_file.read()
    with open("json/GreatSword.json", "r") as json_file:
        json_greatsword_data = json_file.read()
    with open("json/Gunlance.json", "r") as json_file:
        json_gunlance_data = json_file.read()
    with open("json/Hammer.json", "r") as json_file:
        json_hammer_data = json_file.read()
    with open("json/HeavyBowGun.json", "r") as json_file:
        json_heavybowgun_data = json_file.read()
    with open("json/HuntingHorn.json", "r") as json_file:
        json_huntinghorn_data = json_file.read()
    with open("json/InsectGlaive.json", "r") as json_file:
        json_insectglaive_data = json_file.read()
    with open("json/Lance.json", "r") as json_file:
        json_lance_data = json_file.read()
    with open("json/LightBowGun.json", "r") as json_file:
        json_lightbowgun_data = json_file.read()
    with open("json/LongSword.json", "r") as json_file:
        json_longsword_data = json_file.read()
    with open("json/SwitchAxe.json", "r") as json_file:
        json_switchaxe_data = json_file.read()
    with open("json/SwordNShield.json", "r") as json_file:
        json_swordandshield_data = json_file.read()

    bow_data = json.loads(json_bow_data)
    chargeblade_data = json.loads(json_chargeblade_data)
    dualblades_data = json.loads(json_dualblades_data)
    greatsword_data = json.loads(json_greatsword_data)
    gunlance_data = json.loads(json_gunlance_data)
    hammer_data = json.loads(json_hammer_data)
    heavybowgun_data = json.loads(json_heavybowgun_data)
    huntinghorn_data = json.loads(json_huntinghorn_data)
    insectglaive_data = json.loads(json_insectglaive_data)
    lance_data = json.loads(json_lance_data)
    lightbowgun_data = json.loads(json_lightbowgun_data)
    longsword_data = json.loads(json_longsword_data)
    switchaxe_data = json.loads(json_switchaxe_data)
    swordandshield_data = json.loads(json_swordandshield_data)

    id_to_weapon_type = {
        0: 'bow',
        1: 'dualblades',
        2: 'greatsword',
        3: 'longsword',
        4: 'hammer',
        5: 'huntinghorn',
        6: 'lance',
        7: 'gunlance',
        8: 'switchaxe',
        9: 'chargeblade',
        10: 'insectglaive',
        11: 'lightbowgun',
        12: 'heavybowgun',
        13: 'swordandshield'
    }
    armor_data = json.loads(json_armor_data)
    deco_data = json.loads(json_deco_data)
    weapon_data={}
    for weapon_type in id_to_weapon_type.values():
        weapon_data[weapon_type]=eval(f'{weapon_type}_data')


    random.seed(8)
    for k in armor_data.keys():
        random.shuffle(armor_data[k])


    #NON-VAR DATA



    deco_name_to_points={}
    for level in range(4):
        for i in range(len(deco_data['decoLevels'][level])):
            deco_name_to_points[f'{list(deco_data["decoLevels"][level][i].keys())[0]}_{level+1}']=list(deco_data["decoLevels"][level][i].values())[0]



    model = cp_model.CpModel()

    #===========DECLARING VARIABLES================================================================

    #=====CORE VARIABLES======

    #which armor
    id_to_head_armor_var = {id:model.NewBoolVar(f'h{id}') for id in sharded_range_for(shard_index,'helm',len(armor_data['helm'])) }
    id_to_body_armor_var = {id:model.NewBoolVar(f'c{id}') for id in sharded_range_for(shard_index,'chest',len(armor_data['chest'])) }
    id_to_arm_armor_var = {id:model.NewBoolVar(f'a{id}') for id in sharded_range_for(shard_index,'arm',len(armor_data['arm'])) }
    id_to_waist_armor_var = {id:model.NewBoolVar(f'w{id}') for id in sharded_range_for(shard_index,'waist',len(armor_data['waist'])) }
    id_to_leg_armor_var = {id:model.NewBoolVar(f'l{id}') for id in sharded_range_for(shard_index,'leg',len(armor_data['leg'])) }

    #WHICH WEAPON
    weapon_type_vars={i:model.NewBoolVar(f'{i}_twtp') for i in range(14)}
    id_to_weapon_var={i:model.NewBoolVar(f'{i}_whichwpn') for i in range(400)}


    #DECO DISTRIBUTION VARIABLES
    deco_name_to_dist_vars={}
    for level in range(4):
        for pair in deco_data['decoLevels'][level]:
            name=list(pair.keys())[0]
            deco_name_to_dist_vars[f'{name}_{level+1}']=model.NewIntVar(0,3,f'{name}_{level+1}')
                  

    #====INTERMEDIATE VARIABLES=======

    #ARMOR DECO SLOT VARIABLES
    head_deco_slots_vars = [model.NewIntVar(0,3,f'hdeco{i}') for i in range(4)]#number of slots of each level
    body_deco_slots_vars = [model.NewIntVar(0,3,f'bdeco{i}') for i in range(4)]
    arm_deco_slots_vars = [model.NewIntVar(0,3,f'adeco{i}') for i in range(4)]
    waist_deco_slots_vars = [model.NewIntVar(0,3,f'wdeco{i}') for i in range(4)]
    leg_deco_slots_vars = [model.NewIntVar(0,3,f'ldeco{i}') for i in range(4)]

    #WEAPON DECO SLOT VARIABLES
    weapon_deco_slots_vars = [model.NewIntVar(0,3,f'wpndeco{i}') for i in range(4)]


    #ARMOR SKILL VARIABLES
    head_skill_name_to_points_var={skill_name:model.NewIntVar(0,2*deco_data['maxLevel'][skill_name],f'hh{skill_name}') for skill_name in deco_data['maxLevel'].keys()}
    body_skill_name_to_points_var={skill_name:model.NewIntVar(0,2*deco_data['maxLevel'][skill_name],f'bb{skill_name}') for skill_name in deco_data['maxLevel'].keys()}
    arm_skill_name_to_points_var={skill_name:model.NewIntVar(0,2*deco_data['maxLevel'][skill_name],f'aa{skill_name}') for skill_name in deco_data['maxLevel'].keys()}
    waist_skill_name_to_points_var={skill_name:model.NewIntVar(0,2*deco_data['maxLevel'][skill_name],f'www{skill_name}') for skill_name in deco_data['maxLevel'].keys()}
    leg_skill_name_to_points_var={skill_name:model.NewIntVar(0,2*deco_data['maxLevel'][skill_name],f'll{skill_name}') for skill_name in deco_data['maxLevel'].keys()}

    
    #CREATE INTEGER SKILL VARS
    skill_name_to_num_points_var={}
    for skill_name in deco_data['maxLevel'].keys():
        skill_name_to_num_points_var[skill_name]=model.NewIntVar(0,2*deco_data['maxLevel'][skill_name],f'{skill_name}')

    #==============CONSTRAINTS======================================================================

    #OBJECTIVES/OPTIONAL CONSTRAINTS
    #fix weapon
    #model.Add(id_to_weapon_var[0]==1)
    #model.Add(weapon_type_vars[0]==1)

    #skill point constraints
    model.Add(skill_name_to_num_points_var['DragonResistance']>=3)
    model.Add(skill_name_to_num_points_var['GuardUp']>=3)
    model.Add(skill_name_to_num_points_var['Agitator']>=5)
    model.Add(skill_name_to_num_points_var['WeaknessExploit']>=3)
    model.Add(skill_name_to_num_points_var['BladescaleHone']>=3)
    model.Add(skill_name_to_num_points_var['WirebugWhisperer']>=3)
    model.Add(skill_name_to_num_points_var['Bombardier']>=3)
    model.Add(skill_name_to_num_points_var['AffinitySliding']>=1)
    model.Add(skill_name_to_num_points_var['Embolden']>=1)
    model.Add(skill_name_to_num_points_var['Guts']>=2)
    model.Add(skill_name_to_num_points_var['Botanist']>=3)
    model.Add(skill_name_to_num_points_var['Earplugs']>=1)



    #NO DECOS ALLOWED
    '''for level in [0,1,2,3]:
        for pair in deco_data['decoLevels'][level]:
            name=list(pair.keys())[0]
            for part in ['helm','chest','arm','waist','leg','weapon']:
                model.Add(deco_name_to_dist_vars[f'{name}_{level+1}'][part]==0)
    '''

    #========MANDATORY CONSTRAINTS======================================================================


    #===CORE CONSTRAINTS
    #CAN WEAR AT MOST ONE OF EACH ARMOR PIECE
    model.Add(sum(id_to_head_armor_var.values()) == 1)
    model.Add(sum(id_to_body_armor_var.values()) == 1)
    model.Add(sum(id_to_arm_armor_var.values()) == 1)
    model.Add(sum(id_to_waist_armor_var.values()) == 1)
    model.Add(sum(id_to_leg_armor_var.values()) == 1)

    #CAN HAVE AT MOST ONE WEAPON
    model.Add(sum(id_to_weapon_var.values())==1)
    model.Add(sum(weapon_type_vars.values())==1)

    #DECOS CANT EXCEED SLOTS
    for level in range(4):  
        model.Add(sum(deco_name_to_dist_vars[f'{skill_name}_{u_level+1}'] for skill_name in deco_data['decos'] for u_level in range(level,4) if f'{skill_name}_{u_level+1}' in deco_name_to_dist_vars)\
                  
                  <=\
                  
                  sum(head_deco_slots_vars[u_level] for u_level in range(level,4))+\
                  sum(body_deco_slots_vars[u_level] for u_level in range(level,4))+\
                  sum(arm_deco_slots_vars[u_level] for u_level in range(level,4))+\
                  sum(waist_deco_slots_vars[u_level] for u_level in range(level,4))+\
                  sum(leg_deco_slots_vars[u_level] for u_level in range(level,4))+
                  sum(weapon_deco_slots_vars[u_level] for u_level in range(level,4)))


    #====INTERMEDIATE CONSTRAINTS======
    #MAPPING VARIABLES TO JSON ARMOR DATA
    for id in sharded_range_for(shard_index,'helm',len(armor_data['helm'])):
        #MAP DEFENSE VARS
        #model.Add(head_armor_def_var == armor_data['helm'][id]['def']).OnlyEnforceIf(id_to_head_armor_var[id])  
        #MAP HELM ARMOR SKILL POINTS    
        for skill_name in deco_data['maxLevel'].keys():
            if skill_name in armor_data['helm'][id]['skills'].keys():
                model.Add(head_skill_name_to_points_var[skill_name]==armor_data['helm'][id]['skills'][skill_name]).OnlyEnforceIf(id_to_head_armor_var[id])
            else:
                model.Add(head_skill_name_to_points_var[skill_name]==0).OnlyEnforceIf(id_to_head_armor_var[id])
        #MAP HELM ARMOR SLOTS
        for i in range(4):
            model.Add(head_deco_slots_vars[i]==armor_data['helm'][id]['decos'][i]).OnlyEnforceIf(id_to_head_armor_var[id])


    for id in sharded_range_for(shard_index,'chest',len(armor_data['chest'])):
        #model.Add(body_armor_def_var == armor_data['chest'][id]['def']).OnlyEnforceIf(id_to_body_armor_var[id])

        for skill_name in deco_data['maxLevel'].keys():
            if skill_name in armor_data['chest'][id]['skills'].keys():
                model.Add(body_skill_name_to_points_var[skill_name]==armor_data['chest'][id]['skills'][skill_name]).OnlyEnforceIf(id_to_body_armor_var[id])
            else:
                model.Add(body_skill_name_to_points_var[skill_name]==0).OnlyEnforceIf(id_to_body_armor_var[id])

        for i in range(4):
            model.Add(body_deco_slots_vars[i]==armor_data['chest'][id]['decos'][i]).OnlyEnforceIf(id_to_body_armor_var[id])

    for id in sharded_range_for(shard_index,'arm',len(armor_data['arm'])):
        #model.Add(arm_armor_def_var == armor_data['arm'][id]['def']).OnlyEnforceIf(id_to_arm_armor_var[id])

        for skill_name in deco_data['maxLevel'].keys():
            if skill_name in armor_data['arm'][id]['skills'].keys():
                model.Add(arm_skill_name_to_points_var[skill_name]==armor_data['arm'][id]['skills'][skill_name]).OnlyEnforceIf(id_to_arm_armor_var[id])
            else:
                model.Add(arm_skill_name_to_points_var[skill_name]==0).OnlyEnforceIf(id_to_arm_armor_var[id])
        for i in range(4):
            model.Add(arm_deco_slots_vars[i]==armor_data['arm'][id]['decos'][i]).OnlyEnforceIf(id_to_arm_armor_var[id])

    for id in sharded_range_for(shard_index,'waist',len(armor_data['waist'])):
        #model.Add(waist_armor_def_var == armor_data['waist'][id]['def']).OnlyEnforceIf(id_to_waist_armor_var[id])
        for skill_name in deco_data['maxLevel'].keys():
            if skill_name in armor_data['waist'][id]['skills'].keys():
                model.Add(waist_skill_name_to_points_var[skill_name]==armor_data['waist'][id]['skills'][skill_name]).OnlyEnforceIf(id_to_waist_armor_var[id])
            else:
                model.Add(waist_skill_name_to_points_var[skill_name]==0).OnlyEnforceIf(id_to_waist_armor_var[id])
        for i in range(4):
            model.Add(waist_deco_slots_vars[i]==armor_data['waist'][id]['decos'][i]).OnlyEnforceIf(id_to_waist_armor_var[id])

    for id in sharded_range_for(shard_index,'leg',len(armor_data['leg'])):
        #model.Add(leg_armor_def_var == armor_data['leg'][id]['def']).OnlyEnforceIf(id_to_leg_armor_var[id])
        for skill_name in deco_data['maxLevel'].keys():
            if skill_name in armor_data['leg'][id]['skills'].keys():
                model.Add(leg_skill_name_to_points_var[skill_name]==armor_data['leg'][id]['skills'][skill_name]).OnlyEnforceIf(id_to_leg_armor_var[id])
            else:
                model.Add(leg_skill_name_to_points_var[skill_name]==0).OnlyEnforceIf(id_to_leg_armor_var[id])
        for i in range(4):
            model.Add(leg_deco_slots_vars[i]==armor_data['leg'][id]['decos'][i]).OnlyEnforceIf(id_to_leg_armor_var[id])





    #make extra weapon variables zero
    for weapon_type_id,weapon_type in id_to_weapon_type.items():
        numwep = len(eval(f"{weapon_type}_data['weapons']"))
        for x in range(numwep,len(id_to_weapon_var)):
            model.Add((id_to_weapon_var[x])==0).OnlyEnforceIf(weapon_type_vars[weapon_type_id])

    for weapon_type_id,weapon_type in id_to_weapon_type.items():
        for weapon_id in range(len(eval(f"{weapon_type}_data['weapons']"))):

            b = weapon_type_vars[weapon_type_id]
            c = id_to_weapon_var[weapon_id]

            for i in range(4):
                model.Add(weapon_deco_slots_vars[i] == eval(f"{weapon_type}_data['weapons'][{weapon_id}]['decos'][{i}]")).OnlyEnforceIf([b,c])




    #ENFORCING 'skill_name_to_num_points_var' RELATIONSHIP
    for skill_name in deco_data['maxLevel'].keys():
        model.Add(sum(deco_name_to_points[f'{skill_name}_{level+1}']*deco_name_to_dist_vars[f'{skill_name}_{level+1}'] for level in [0,1,2,3] if f'{skill_name}_{level+1}' in deco_name_to_dist_vars)+\
            
            (head_skill_name_to_points_var[skill_name] +  \
            body_skill_name_to_points_var[skill_name] +  \
            arm_skill_name_to_points_var[skill_name]  +  \
            waist_skill_name_to_points_var[skill_name]+  \
            leg_skill_name_to_points_var[skill_name]) == \
            skill_name_to_num_points_var[skill_name])


    #===========CREATING SOLVER AND SOLUTION PRINTER================================================================================
    solver = cp_model.CpSolver()
 
    solver.parameters.num_search_workers=1
    solution_printer_arg={
    "id_to_head_armor_var": id_to_head_armor_var,
    "id_to_body_armor_var": id_to_body_armor_var,
    "id_to_arm_armor_var": id_to_arm_armor_var,
    "id_to_waist_armor_var": id_to_waist_armor_var,
    "id_to_leg_armor_var": id_to_leg_armor_var,
    "armor_data": armor_data,
    "deco_name_to_dist_vars": deco_name_to_dist_vars,
    "deco_data": deco_data,
    'weapon_data':weapon_data,
    'id_to_weapon_var':id_to_weapon_var,
    'weapon_type_vars':weapon_type_vars,
    'id_to_weapon_type':id_to_weapon_type,
    'weapon_type_vars':weapon_type_vars
    }
    solution_printer = VarArraySolutionPrinter(solution_printer_arg)

    #=================SOLVING===========================================================================


    solver.parameters.enumerate_all_solutions = True

    status = solver.Solve(model,solution_callback=solution_printer)
    #print(f'process {shard_index} ended')


    #==============PRINT WHETHER FOUND OPTIMAL SOLUTION====================================================
    '''    if status == cp_model.OPTIMAL:
            print('\n' + "Optimal solution found!" + '\n')
        elif status == cp_model.FEASIBLE:
            print('\n' + "A solution found, but may not be optimal." + '\n')
        else:
            print('\n' + "No solution found!" + '\n')
    '''




    #TODO
    '''Reduce the amount of variables.
    Reduce the domain of the integer variables.
    Run the solver with multiples threads usingsolver.parameters.num_search_workers = 8.
    Prefer boolean over integer variables/contraints.
    Set redundant constraints and/or symmetry breaking constraints.
    Segregate your problem and merge the results.



    You cannot inside the solver. You need to parallelize it yourself.
    model.AddDecisionStrategy(
            task_starts, cp_model.CHOOSE_LOWEST_MIN, cp_model.SELECT_MIN_VALUE)
    '''