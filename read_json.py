import json
all_weapons=['great_sword','short_sword','hammer','lance','long_sword','slash_axe','gun_lance','dual_blades','horn','insect_glaive','charge_axe','light_bowgun','heavy_bowgun','bow']
all_weapons_cap=['GreatSword','ShortSword','Hammer','Lance','LongSword', 'SlashAxe','GunLance','DualBlades','Horn','InsectGlaive','ChargeAxe','LightBowgun','HeavyBowgun','Bow']


from thefuzz import fuzz
from thefuzz import process



# Open the JSON file and read its content
with open("mhrice.json", "r") as json_file:
    json_data = json_file.read()

# Parse the JSON data into a Python dictionary
parsed_data = json.loads(json_data)
print('DATA PARSED')


print(len(parsed_data["great_sword"]['base_data']['param']))
print(len(parsed_data["great_sword"]['name']['entries']))
print(len(parsed_data["great_sword"]['name_mr']['entries']))


for weapon_type in ['great_sword']:#doesn't work from lbg to bow(ranged weapons)

    weapon_type_cap=process.extractOne(weapon_type, all_weapons_cap)[0]

    for i in range(294):    
        weapon_info_dict = parsed_data[weapon_type]['base_data']['param'][i]['base']
        id = weapon_info_dict['base']['base']['base']['id'][weapon_type_cap]
        name_key = 'name'
        if id >= 300:
            id = id % 300
            name_key = 'name_mr'

        name = parsed_data[weapon_type][name_key]['entries'][id]
        realname = parsed_data[weapon_type][name_key]['entries'][id]['content'][1]
        raw =               weapon_info_dict['base']['base']['atk']
        affinity =          weapon_info_dict['base']['base']['critical_rate']
        sharpness =         weapon_info_dict['sharpness_val_list']
        def_bonus =         weapon_info_dict['base']['base']['def_bonus']

        normal_deco_slots = weapon_info_dict['base']['base']['slot_num_list']
        rampage_deco_slots =weapon_info_dict['base']['base']['hyakuryu_slot_num_list']
        if len(weapon_info_dict['base']['base']['hyakuryu_skill_id_list'])==0 or\
        weapon_info_dict['base']['base']['hyakuryu_skill_id_list'][0]=="None":
            continue
        rampage_skill_ids = [d['Skill'] for d in parsed_data[weapon_type]['base_data']['param'][i]['base']['base']['base']['hyakuryu_skill_id_list']]
        
        rampage_skill_names = [parsed_data['hyakuryu_skill_name_msg']['entries'][rid + 1]['content'][1] for rid in rampage_skill_ids]

        print(i,':::::',realname, rampage_skill_names, raw)

#weapons start at line 2394640
#use the weeapontype to number as id in  w thingy.