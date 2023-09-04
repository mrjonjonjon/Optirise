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
