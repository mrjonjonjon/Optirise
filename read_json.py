import json
all_weapons=['great_sword','short_sword','hammer','lance','long_sword','slash_axe','gun_lance','dual_blades','horn','insect_glaive','charge_axe','light_bowgun','heavy_bowgun','bow']
all_weapons_cap=['GreatSword','ShortSword','Hammer','Lance','LongSword', 'SlashAxe','GunLance','DualBlades','Horn','InsectGlaive','ChargeAxe','LightBowgun','HeavyBowgun','Bow']


from thefuzz import fuzz
from thefuzz import process

import utils

# Open the JSON file and read its content
with open("mhrice.json", "r") as json_file:
    json_data = json_file.read()

# Parse the JSON data into a Python dictionary
parsed_data = json.loads(json_data)
print('DATA PARSED')

test_type='gun_lance'

print('BASE DATA: ',len(parsed_data[test_type]['base_data']['param']))
print('NAME: ',len(parsed_data[test_type]['name']['entries']))
print('NAME_MR: ',len(parsed_data[test_type]['name_mr']['entries']))
print('NAME+NAME_MR: ',len(parsed_data[test_type]['name']['entries'])+len(parsed_data[test_type]['name_mr']['entries']))
print('EXPLAIN ',len(parsed_data[test_type]['explain']['entries']))

all_ids=[]
all_name_ids=[]
all_name_ids2=[]
for name in parsed_data[test_type]['name']['entries']:
    all_name_ids.append(utils.extract_number(name['name']))
for name in parsed_data[test_type]['name_mr']['entries']:
    all_name_ids.append(utils.extract_number(name['name']))

print('ALL NAME_IDS: ',utils.generate_intervals(all_name_ids),(sum([b-a+1 for a,b in utils.generate_intervals(all_name_ids)])))

count=0

maxraw=0
maxrawweapon='ytgfiyghiuyv'
for weapon_type in [test_type]:#doesn't work from lbg to bow(ranged weapons)

    weapon_type_cap=process.extractOne(weapon_type, all_weapons_cap)[0]

    for i in range(len(parsed_data[weapon_type]['base_data']['param'])):    
        weapon_info_dict = parsed_data[weapon_type]['base_data']['param'][i]['base']
        id = weapon_info_dict['base']['base']['base']['id'][weapon_type_cap]
   
        name_key = 'name'
        all_ids.append(id)
        if id >= 300:
            id = id % 300
            name_key = 'name_mr'

        name = parsed_data[weapon_type][name_key]['entries'][id]['name']
        name_id=utils.extract_number(name)
        all_name_ids.append(name_id)
        realname = parsed_data[weapon_type][name_key]['entries'][id]['content'][1]
        if len(realname)==0:continue
        if realname[0]=='<':continue
        raw =               weapon_info_dict['base']['base']['atk']
        if raw ==0:
            count+=1
            continue
        element_type = weapon_info_dict['base']['main_element_type']
        element_damage = weapon_info_dict['base']['main_element_val']
        affinity =          weapon_info_dict['base']['base']['critical_rate']
        sharpness =         weapon_info_dict['sharpness_val_list']
        def_bonus =         weapon_info_dict['base']['base']['def_bonus']
        normal_deco_slots = weapon_info_dict['base']['base']['slot_num_list']
        rampage_deco_slots =weapon_info_dict['base']['base']['hyakuryu_slot_num_list']
        rampage_skill_ids=[]
        if len(weapon_info_dict['base']['base']['hyakuryu_skill_id_list'])==0 or\
        weapon_info_dict['base']['base']['hyakuryu_skill_id_list'][0]=="None":
            rampage_skill_ids=[]
        else:
            rampage_skill_ids = [d['Skill'] for d in parsed_data[weapon_type]['base_data']['param'][i]['base']['base']['base']['hyakuryu_skill_id_list']]
        
        rampage_skill_names = [parsed_data['hyakuryu_skill_name_msg']['entries'][rid + 1]['content'][1] for rid in rampage_skill_ids]


        if raw>maxraw:
            maxraw=raw
            maxrawweapon=realname
        #print(i,':::::',realname, rampage_skill_names, raw,affinity)
print('BASE DATA RAW=0: ',count)
print('MAX RAW: ',maxrawweapon,',,,,',maxraw)
print('ALL IDS: ',utils.generate_intervals(all_ids),(sum([b-a+1 for a,b in utils.generate_intervals(all_ids)])))
#print('ALL NAME_IDS: ',utils.generate_intervals(all_name_ids),(sum([b-a+1 for a,b in utils.generate_intervals(all_name_ids)])))

#weapons start at line 2394640
#use the weeapontype to number as id in  w thingy.

#last gunlance id is 482
#308->437
#gunlance id 137 is duplicated once
#"name" map is well organized except for extraneous 137 at end of name_mr