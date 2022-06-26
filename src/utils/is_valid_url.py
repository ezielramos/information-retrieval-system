from urllib.parse import urlparse

def is_valid_url(url:str) -> bool:
    try:
        result = urlparse(url)
        _ = all([ result.scheme, result.netloc, result.path ])
    except:
        return False
    return True