import math

def relevance_function(value):
    if value > 0.5:
        value = 1
    elif value > 0.3 and value <= 0.5:
        value = 2
    elif value > 0.2 and value <= 0.3:
        value = 3
    elif value >= 0.125 and value <= 0.2:
        value = 4
    else:
        value = 5

    return value

def get_similarity(vector_query, vector_document):
    numerador = 0
    norm_query = 0
    norm_document = 0

    for query in vector_query:
        if vector_document.get(query) != None:
            numerador += vector_query[query] * vector_document[query]
        norm_query += vector_query[query] ** 2
    for doc in vector_document:
        norm_document += vector_document[doc] ** 2

    if (math.sqrt(norm_query) * math.sqrt(norm_document)) == 0:
        return 0
    else:
        return numerador / (math.sqrt(norm_query) * math.sqrt(norm_document))

def get_rank(queries_weight, documents_weight):
    rank = []
    cquery = 0

    for item in queries_weight:
        cquery += 1
        temp = []
        if len(item) > 0:
            for element in documents_weight:
                if len(element[1]) == 0:
                    break
                similarity = get_similarity(item, element[1])
                sim = relevance_function(similarity)
                if sim < 5:
                    temp.append((cquery, element[0], sim))
            temp.sort(key=lambda x:x[2])
        rank.append(temp)

    return rank

def print_rank(rankList):
    for item in rankList:
        for element in item:
            if element[2] <= 5:
                print('consulta = ' + str(element[0]) + ' documento = ' + str(element[1]) + ' similitud = ' + str(element[2]))

    print()
