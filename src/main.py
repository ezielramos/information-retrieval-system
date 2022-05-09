from tools.tools import *

def documents_analyser(path):

    tf, idf, documents_list = get_matrix_df_idf(path)
    weight = get_matrix_weight(tf, idf, lambda x, y : x * y, documents_list)

    return weight

def queries_analyser(path, a=0.5):
    
    tf, idf, _ = get_matrix_df_idf(path)
    weight = get_matrix_weight(tf, idf, lambda x , y : y * ((a + (1 - a) * x)))

    return weight

def main():

    queries_path = 'collections/cran/cran.qry'
    documents_path = 'collections/cran/cran.all'
    answers_path = 'collections/cran/cranqrel'

    documents_weight = documents_analyser(documents_path)
    print(f'documents_weight = {documents_weight}\n')

    queries_weight = queries_analyser(queries_path)
    print(f'queries_weight = {queries_weight}\n')
    
if __name__ == '__main__':
    main()