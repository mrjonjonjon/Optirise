def no_decos():
    #NO DECOS ALLOWED
    exec(
    '''for level in [0,1,2,3]:
        for pair in deco_data['decoLevels'][level]:
            name=list(pair.keys())[0]
            for part in ['helm','chest','arm','waist','leg','weapon']:
                model.Add(deco_name_to_dist_vars[f'{name}_{level+1}'][part]==0)
    ''')