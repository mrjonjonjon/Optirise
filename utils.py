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
    b4_string=to_base_4(idx)
    shard_index>>=idx
    b=-1
    if abs(-1-idx)>len(b4_string):
        b=0
    else:
        b= int(b4_string[-1-idx])
    return sharded_range(b,4,len_lst)




def sharded_range(shard_index,num_shards,len_lst):
    return range(shard_index  *  len_lst//num_shards,\
                       ((shard_index+1)  *len_lst//num_shards) if shard_index<num_shards-1 else len_lst)
all_weapons_cap=['GreatSword','ShortSword','Hammer','Lance','LongSword', 'SlashAxe','GunLance','DualBlades','Horn','InsectGlaive','ChargeAxe','LightBowgun','HeavyBowgun','Bow']
