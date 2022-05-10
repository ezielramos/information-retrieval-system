

def welcome():

    while True:

        option = print_welcome()
        if option >= 1 and option <= 5:
            break
        else:
            print('Por favor, selecciona una opción válida\n')

    return option

def print_welcome():

    print('BIENVENIDO AL SISTEMA DE RECUPERACIÓN DE INFORMACIÓN\n')
    print('Escoja la opción deseada:')
    print('1. Procesar las consultas de la colección de datos')
    print('2. Realizar una consulta nueva sobre la colección de datos')
    print('3. Imprimir la información de los desarrolladores')
    print('4. Imprimir la información de la aplicación')
    print('5. Salir')
    option = int(input())

    return option