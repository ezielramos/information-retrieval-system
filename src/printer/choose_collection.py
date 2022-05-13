

def choose_collection():

    while True:

        option = print_choose_collection()
        if option >= 1 and option <= 2:
            break
        else:
            print('Por favor, selecciona una opción válida\n')

    return option

def print_choose_collection():

    print('\nBIENVENIDO AL SISTEMA DE RECUPERACIÓN DE INFORMACIÓN\n')
    print('Escoja la colección de datos deseada:')
    print('1. CRANFIELD')
    print('2. CISI')
    option = int(input())

    return option
