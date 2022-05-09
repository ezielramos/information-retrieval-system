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

def get_rr_ri_nr(path, recovered):
    recovered_list = recovered_colection(path)
    relevant_retrieved = 0
    irrelevant_retrieved = 0

    for item in recovered:
        for element in item:
            temp = (element[0], element[1])
            try:
                recovered_list.remove(temp)
                relevant_retrieved += 1
            except:
                irrelevant_retrieved += 1

    non_irrelevant_retrieved = len(recovered_list)
    return relevant_retrieved, irrelevant_retrieved, non_irrelevant_retrieved

def recovered_colection(path):

    lines = read_file(path)
    recovered_list = []

    for line in lines:
        temp = turn_line_to_words(line)
        temp = list(temp.items())
        recovered_list.append((int(temp[0][0]), int(temp[1][0])))

    print(f'recovered_list = {recovered_list}\n')
    return recovered_list

def turn_line_to_words(line):
    word_list,word = {},''

    for item in line:
        if (item == ' ' or item == '\n' or item == '\t') and len(word) > 0:
            if word_list.get(word) == None:
                word_list[word] = 1
            else:
                word_list[word] += 1
            word = ''
        elif item != ' ':
            word += item

    if len(word) > 0:
        if word_list.get(word) == None:
            word_list[word] = 1
        else:
            word_list[word] += 1

    return word_list
