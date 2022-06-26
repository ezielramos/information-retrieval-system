

def prefix_funtion(patron:str) -> list:
    pi, k = [ 0 for _ in patron ], 0
    for i in range(2, len(patron)):
        while k>0 and patron[k+1] != patron[i]:
            k = pi[k]
        if patron[k+1] == patron[i]:
            k += 1
        pi[i] = k
    return pi

def kmp(text:str, patron:str) -> list:
    ocurrencies, k = [], 0
    pi = prefix_funtion(patron)

    for i in range(1, len(text)):
        while k>0 and text[i] != patron[k+1]:
            k = pi[k]
        if text[i] == patron[k+1]:
            k += 1
        if k == len(patron) - 1:
            k = pi[k]
            ocurrencies.append(i - len(patron) + 1)

    return ocurrencies