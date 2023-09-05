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


import re

def extract_number(s):
    match = re.search(r'(\d+)', s)
    if match:
        return int(match.group(1))
    else:
        return None


def write_list_to_json(lst,filename):
    import json
    with open(filename, 'w') as file:
        json.dump(lst, file)


def read_json_list(filename):
    import json
    with open(filename, 'r') as file:
        lst = json.load(file)
        return lst

#assumes 8 shards
def sharded_range_for(shard_index,part,len_lst):
    idx = ['helm','chest','arm'].index(part)
    shard_index>>=idx
    b= shard_index&1
    return sharded_range(b,2,len_lst)




def sharded_range(shard_index,num_shards,len_lst):
    return range(shard_index  *  len_lst//num_shards,\
                       ((shard_index+1)  *len_lst//num_shards) if shard_index<num_shards-1 else len_lst)
all_weapons_cap=['GreatSword','ShortSword','Hammer','Lance','LongSword', 'SlashAxe','GunLance','DualBlades','Horn','InsectGlaive','ChargeAxe','LightBowgun','HeavyBowgun','Bow']
