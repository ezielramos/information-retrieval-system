

def get_standard_str(id):
    str_id = str(id)
    if len(str_id) == 1:
        return f'00{id}'
    elif len(str_id) == 2:
        return f'0{id}'
    else:
        return f'{id}'