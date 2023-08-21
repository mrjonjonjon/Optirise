import json
all_weapons=['great_sword','short_sword','hammer','lance','long_sword','slash_axe','gun_lance','dual_blades','horn','insect_glaive','charge_axe','light_bowgun','heavy_bowgun','bow']
# Open the JSON file and read its content
with open("mhrice.json", "r") as json_file:
    json_data = json_file.read()

# Parse the JSON data into a Python dictionary
parsed_data = json.loads(json_data)
print('DATA PARSED')


print(len(parsed_data["great_sword"]['base_data']['param']))
print(len(parsed_data["great_sword"]['name']['entries']))
for i in range(10):
    id = parsed_data["great_sword"]['base_data']['param'][i]['base']['base']['base']['base']['id']['GreatSword']
    if id>=300:
        id=id%300
        name = parsed_data["great_sword"]['name_mr']['entries'][id]
        realname = parsed_data["great_sword"]['name_mr']['entries'][id]['content'][1]
        raw = parsed_data["great_sword"]['base_data']['param'][i]['base']['base']['base']['atk']
        affinity = parsed_data["great_sword"]['base_data']['param'][i]['base']['base']['base']['critical_rate']
        normal_deco_slots = parsed_data["great_sword"]['base_data']['param'][i]['base']['base']['base']['slot_num_list']
        rampage_deco_slots = parsed_data["great_sword"]['base_data']['param'][i]['base']['base']['base']['hyakuryu_slot_num_list']
        rampage_skill_ids=[d['Skill'] for d in parsed_data["great_sword"]['base_data']['param'][i]['base']['base']['base']['hyakuryu_skill_id_list']]
        rampage_skill_names = [parsed_data['hyakuryu_skill_name_msg']['entries'][rid+1]['content'][1] for rid in rampage_skill_ids]
        print(realname,rampage_skill_names,'\n\n')
    else:
        name = parsed_data["great_sword"]['name']['entries'][id]
        realname = parsed_data["great_sword"]['name']['entries'][id]['content'][1]
        raw = parsed_data["great_sword"]['base_data']['param'][i]['base']['base']['base']['atk']
        affinity = parsed_data["great_sword"]['base_data']['param'][i]['base']['base']['base']['critical_rate']
        normal_deco_slots = parsed_data["great_sword"]['base_data']['param'][i]['base']['base']['base']['slot_num_list']
        rampage_deco_slots = parsed_data["great_sword"]['base_data']['param'][i]['base']['base']['base']['hyakuryu_slot_num_list']
        rampage_skill_ids=[d['Skill'] for d in parsed_data["great_sword"]['base_data']['param'][i]['base']['base']['base']['hyakuryu_skill_id_list']]
        rampage_skill_names = [parsed_data['hyakuryu_skill_name_msg']['entries'][rid+1]['content'][1] for rid in rampage_skill_ids]
        print(realname,rampage_skill_names,'\n\n')

#weapons star at line 2394640
#use the weeapontype to number as id in  w thingy.