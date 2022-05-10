from tools.tools import *
from tools.similarity import *
from evaluation_system.precision_measurements import *

def documents_analyser(path):

    tf, idf, documents_list = get_matrix_df_idf(path)
    weight = get_matrix_weight(tf, idf, lambda x, y : x * y, documents_list)

    return weight

def queries_analyser(path, a=0.5):
    
    tf, idf, _ = get_matrix_df_idf(path)
    weight = get_matrix_weight(tf, idf, lambda x , y : y * ((a + (1 - a) * x)))

    return weight

def answers_analyser(path, rank, total_doc):

    rr, ri, nr = get_rr_ri_nr_ni(path, rank, total_doc)

    precision = PrecisionMeasurements.GetPrecision(rr, ri)
    recovered = PrecisionMeasurements.GetRecovered(rr, nr)
    
    if rr != 0:
        measure_f1 = PrecisionMeasurements.GetMearureF(precision, recovered, beta=1)
    else:
        measure_f1 = ' '

    return precision, recovered, measure_f1

def analyser(documents_path, queries_path, answers_path, total_doc):

    documents_weight = documents_analyser(documents_path)
    # print(f'documents_weight = {documents_weight}\n')

    queries_weight = queries_analyser(queries_path)
    # print(f'queries_weight = {queries_weight}\n')
    
    rank = get_rank(queries_weight, documents_weight)
    # print(f'rank = {rank}\n')

    # print_rank(rank)

    precision, recovered, measure_f1 = answers_analyser(answers_path, rank, total_doc)

    print('\nIMPRIMIENDO MEDIDAS DE EVALUACÓN\n')
    print(f'Precisión = {precision}')
    print(f'Recobrado = {recovered}')
    print(f'Medida F1 = {measure_f1}')
