import json

lst = [1, 2, 3, 4, 5]

import utils

utils.write_list_to_json(lst,'jjj.json')
print(utils.read_json_list('jjj.json'))