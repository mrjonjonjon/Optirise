def generate_intervals(nums):
    # Sort the numbers
    sorted_nums = sorted(nums)

    # If the list is empty, return an empty list of intervals
    if not sorted_nums:
        return []

    intervals = []
    start = sorted_nums[0]
    end = sorted_nums[0]

    for num in sorted_nums[1:]:
        # If the current number is consecutive to the previous one
        if num == end + 1:
            end = num
        else:
            # Otherwise, append the interval found so far and start a new one
            intervals.append((start, end))
            start, end = num, num

    # Append the last interval
    intervals.append((start, end))

    return intervals
from collections import defaultdict

import re

def extract_number(s):
    match = re.search(r'(\d+)', s)
    if match:
        return int(match.group(1))
    else:
        return None


def to_base_4(n):
    """Convert a number to base 4."""
    if n == 0:
        return '0'
    digits = []
    while n:
        digits.append(str(n % 4))
        n //= 4
    # Return the number in base 4 as a string
    return ''.join(digits[::-1])

def ith_digit_base_4(n, i):
    """Convert a number to base 4 and get the ith digit."""
    base_4_str = to_base_4(n)
    if i < 0 or i >= len(base_4_str):
        return None
    return int(base_4_str[i])





def write_list_to_json(lst,filename):
    import json
    with open(filename, 'w') as file:
        json.dump(lst, file)


def read_json_list(filename):
    import json
    with open(filename, 'r') as file:
        lst = json.load(file)
        return lst

#assumes 2**5 shards
def sharded_range_for(shard_index,part,len_lst):
    idx = ['helm','chest','arm','waist','leg'].index(part)
    shard_index>>=idx
    b= shard_index&1
    return sharded_range(b,2,len_lst)


def distribute_decos(selected_deco_names,selected_helm_armor_id,selected_body_armor_id,selected_arm_armor_id,selected_waist_armor_id,selected_leg_armor_id,armor_data,deco_data):
    deco_levels=defaultdict(list)
    final_dist=defaultdict(list)
    for deco_name in selected_deco_names:
        name,level=deco_name.split('_')
        deco_levels[int(level)].append(name)

    armor_levels=defaultdict(list)
    for part in ['helm','body','arm','waist','leg']:
        for slot_level,num in enumerate(eval(f'armor_data[{part}][selected_{part}_armor_id]')):
            for i in range(num):
                armor_levels[slot_level+1].append(part)

    for deco_level in range(4,0,-1):
        for deco_name in deco_levels[deco_level]:
            if len(armor_levels[deco_level])>0:
                part_to_use=armor_levels[deco_level][-1]
                armor_levels[deco_level].pop()

                final_dist[part_to_use].append(deco_name)
            else:
                return 'IMPOSSIBLE'
    return final_dist

def sharded_range(shard_index,num_shards,len_lst):
    return range(shard_index  *  len_lst//num_shards,\
                       ((shard_index+1)  *len_lst//num_shards) if shard_index<num_shards-1 else len_lst)
all_weapons_cap=['GreatSword','ShortSword','Hammer','Lance','LongSword', 'SlashAxe','GunLance','DualBlades','Horn','InsectGlaive','ChargeAxe','LightBowgun','HeavyBowgun','Bow']
