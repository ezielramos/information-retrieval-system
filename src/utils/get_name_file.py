

def get_name_file(count):
    name_file = ''
    s = str(count)

    if len(s) == 1:
        name_file = f'000{s}'
    elif len(s) == 2:
        name_file = f'00{s}'
    elif len(s) == 3:
        name_file = f'0{s}'
    else:
        name_file = s

    return name_file