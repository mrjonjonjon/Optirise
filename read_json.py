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


for weapon_type in ['great_sword']:

    weapon_type_cap=process.extractOne(weapon_type, all_weapons_cap)[0]

    for i in range(294):
        id = parsed_data[weapon_type]['base_data']['param'][i]['base']['base']['base']['base']['id'][weapon_type_cap]
        if id >= 300:
            id = id % 300
            name = parsed_data[weapon_type]['name_mr']['entries'][id]
            realname = parsed_data[weapon_type]['name_mr']['entries'][id]['content'][1]
            raw =               parsed_data[weapon_type]['base_data']['param'][i]['base']['base']['base']['atk']
            affinity =          parsed_data[weapon_type]['base_data']['param'][i]['base']['base']['base']['critical_rate']
            sharpness =         parsed_data[weapon_type]['base_data']['param'][i]['base']['sharpness_val_list']
            def_bonus =         parsed_data[weapon_type]['base_data']['param'][i]['base']['base']['base']['def_bonus']

            normal_deco_slots = parsed_data[weapon_type]['base_data']['param'][i]['base']['base']['base']['slot_num_list']
            rampage_deco_slots =parsed_data[weapon_type]['base_data']['param'][i]['base']['base']['base']['hyakuryu_slot_num_list']
            if parsed_data[weapon_type]['base_data']['param'][i]['base']['base']['base']['hyakuryu_skill_id_list'][0]=="None" or \
                (parsed_data[weapon_type]['base_data']['param'][i]['base']['base']['base']['hyakuryu_skill_id_list'])==0:
                continue
            rampage_skill_ids = [d['Skill'] for d in parsed_data[weapon_type]['base_data']['param'][i]['base']['base']['base']['hyakuryu_skill_id_list']]
            
            rampage_skill_names = [parsed_data['hyakuryu_skill_name_msg']['entries'][rid + 1]['content'][1] for rid in rampage_skill_ids]

            print(i,':::::',realname, rampage_skill_names, raw)
        else:
            name = parsed_data[weapon_type]['name']['entries'][id]
            realname = parsed_data[weapon_type]['name']['entries'][id]['content'][1]
            raw = parsed_data[weapon_type]['base_data']['param'][i]['base']['base']['base']['atk']
            affinity = parsed_data[weapon_type]['base_data']['param'][i]['base']['base']['base']['critical_rate']
            sharpness = parsed_data[weapon_type]['base_data']['param'][i]['base']['sharpness_val_list']
            def_bonus =         parsed_data[weapon_type]['base_data']['param'][i]['base']['base']['base']['def_bonus']

            normal_deco_slots = parsed_data[weapon_type]['base_data']['param'][i]['base']['base']['base']['slot_num_list']
            rampage_deco_slots = parsed_data[weapon_type]['base_data']['param'][i]['base']['base']['base']['hyakuryu_slot_num_list']
            if parsed_data[weapon_type]['base_data']['param'][i]['base']['base']['base']['hyakuryu_skill_id_list'][0]=="None" or \
                (parsed_data[weapon_type]['base_data']['param'][i]['base']['base']['base']['hyakuryu_skill_id_list'])==0:
                continue
            rampage_skill_ids = [d['Skill'] for d in parsed_data[weapon_type]['base_data']['param'][i]['base']['base']['base']['hyakuryu_skill_id_list'] if d['Skill']!='None']
            rampage_skill_names = [parsed_data['hyakuryu_skill_name_msg']['entries'][rid + 1]['content'][1] for rid in rampage_skill_ids]
            print(i,'::::::',realname, rampage_skill_names, raw)

#weapons start at line 2394640
#use the weeapontype to number as id in  w thingy.