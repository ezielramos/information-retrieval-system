from tools.analyser import *

from printer.welcome import welcome
from printer.app_info import app_info
from printer.choose_collection import choose_collection
from printer.developments_info import developments_info

def get_query():

    print('Imrima la consulta deseada:')
    query = input()
    return query

def cran():

    documents_path = 'collections/cran/cran.all'
    queries_path = 'collections/cran/cran.qry'
    answers_path = 'collections/cran/cran.rel'

    analyser(documents_path, queries_path, answers_path, 1400)
    print()

def cisi():
    documents_path = 'collections/cisi/cisi.all'
    queries_path = 'collections/cisi/cisi.qry'
    answers_path = 'collections/cisi/cisi.rel'

    analyser(documents_path, queries_path, answers_path, 1460)
    print()

def main():

    while True:

        option = welcome()

        if option == 1:
            collection = choose_collection()
            if collection == 1:
                cran()
            else:
                cisi()
        elif option == 2:
            # query = get_query()
            # process_query(query)
            pass
        elif option == 3:
            developments_info()
        elif option == 4:
            app_info()
        else:
            return

if __name__ == '__main__':
    main()