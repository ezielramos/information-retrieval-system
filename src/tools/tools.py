import math

from tools.tokenizer import tokenize
from tools.tokenizer import read_file

def get_matrix_idf(documents_list, documents_words, documents_count):
    idf = {}
    for word in documents_words:
        # buscar en cuantos documentos aparece la palabra 'documents_words[word]'
        count_doc = get_count_documents(documents_list, word)
        idf[word] = math.log10(documents_count / count_doc)
    return idf

def get_count_documents(documents_list, word):
    count = 0
    for doc in documents_list:
        frecuency_words = doc[1]
        if word in frecuency_words:
            count += 1
    return count

def get_matrix_tf(documents_list, documents_maximum):
    tf = []
    for idx,doc in enumerate(documents_list):
        row_tf = {}
        frecuency_words = doc[1]
        for key in frecuency_words.keys():
            row_tf[key] = frecuency_words[key] / documents_maximum[idx]
        tf.append(row_tf.copy())

    return tf

def get_matrix_weight(tf, idf, function, document_list=[]):
    weight = []
    for i in range(len(tf)):
        temp = {}
        for j in idf:
            if tf[i].get(j) != None:
                term = tf[i][j]
                temp[j] = function(term, idf[j])
        if len(document_list) > 0:
            weight.append((document_list[i][0], temp))
        else:
            weight.append(temp)

    return weight

def get_matrix_df_idf(path):

    lines = read_file(path)
    documents_words, documents_list, documents_count, documents_maximum = tokenize(lines)

    print(f'documents_words = {documents_words}\n')
    print(f'documents_list = {documents_list}\n')
    print(f'documents_count = {documents_count}\n')
    print(f'documents_maximum = {documents_maximum}\n')

    tf = get_matrix_tf(documents_list, documents_maximum)
    idf = get_matrix_idf(documents_list, documents_words, documents_count)

    return tf, idf, documents_list

