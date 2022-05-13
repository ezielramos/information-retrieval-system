from printer.welcome import welcome
from printer.app_info import app_info
from printer.choose_collection import choose_collection
from printer.developments_info import developments_info

from cranfield.cranfield import cranfield
from cranfield.cranfield_manual_query import cranfield_manual_query

from cisi.cisi import cisi
from cisi.cisi_manual_query import cisi_manual_query

def analyser_cranfield():
    cranfield()

def analyser_cranfield_manual_query():
    print('\nEscriba la consulta deseada:', end=' ')
    query = input()

    cranfield_manual_query(query)

def analyser_cisi():
    cisi()

def analyser_cisi_manual_query():
    print('\nEscriba la consulta deseada:', end=' ')
    query = input()

    cisi_manual_query(query)

def main():

    while True:

        option = welcome()

        if option == 1:
            collection = choose_collection()
            if collection == 1:
                cranfield()
            else:
                cisi()

        elif option == 2:
            collection = choose_collection()
            if collection == 1:
                analyser_cranfield_manual_query()
            else:
                analyser_cisi_manual_query()

        elif option == 3:
            developments_info()

        elif option == 4:
            app_info()

        else:
            return

if __name__ == '__main__':
    main()