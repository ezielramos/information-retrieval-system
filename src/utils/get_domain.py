

def get_domain(url:str) -> str:
    split_url = url.split('/')
    file_name = split_url[-1]
    split_file_name = file_name.split('.')
    if split_file_name[0] == 'www':
        domain = '.'.join(split_file_name[1:])
        return domain
    return file_name