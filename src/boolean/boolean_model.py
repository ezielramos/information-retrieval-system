import re
import streamlit as st

def processFile(corpus):
    '''
    This function opens and reads the file, also it does a split when 
    finding a line break before an .I
    '''
    with open(corpus, 'r') as file:
        contents = file.read()
        docs = contents.split('\n.I')
    return docs

def cleanDocs(corpus):
    '''
    This function deletes the line breaks, upper letters, slash, parenthesis, numbers, commas, dots, etc. and put the documents in a list, each element of the list is a document.
    '''
    alldocs = processFile(corpus)
    sinSaltos = ([doc.replace('\n',' ') for doc in alldocs])
    sinMayus = [re.sub('[ITABW]', ' ', doc) for doc in sinSaltos]
    sinSlash = [re.sub('/', '', doc) for doc in sinMayus]
    sinParent1 = ([doc.replace('(','') for doc in sinSlash])
    sinParent2 = ([doc.replace(')','') for doc in sinParent1])
    sinNums = [re.sub(r'\d', '', doc) for doc in sinParent2]
    sinComas = ([doc.replace(',','') for doc in sinNums])
    sinSignos = [re.sub(r'^\w+\.\s?', ' ', doc) for doc in sinComas]
    sinPalabrasComp = ([doc.replace('-',' ') for doc in sinSignos])
    clean = [" ".join(filter(str.isalpha,x.split(" "))) for x in sinPalabrasComp]
    
    return clean

def createDictionary(corpus):
    '''
    This function creates the dictionary.
    '''
    docs = cleanDocs(corpus)                                # list of clean documents
    dictionary = {}                                         # this will be our dictionary with terms and posting lists
    termCount = {}                                          # dictionary that will contain the frequency of the terms
    for index, doc in enumerate(docs):                      # iterate over the index(key of a document) and value of an item (text of document) in a list (of clean documents). It means we put an index(key) to every document in the list.
        for term in doc.split():                            # do an split to each term in the document (Tokenize)
            termCount[term] = termCount.get(term,0) + 1     # tell us how many times each term occurs and put in the termCount dictionary each term with their frequency
            if dictionary.get(term,False):                  # if the dictionary has a term(key) but not a value (posting list)
                if index not in dictionary[term]:           # if the index(key of the document) is not in the posting list
                    dictionary[term].append(index)          # add the index(key of the document) to the posting list
            else:                                           # if the term or key has a value (a document, posting list)
                dictionary[term] = [index]                  # the posting list will be the index (key of the document)
    return dictionary

def searchTerms(term, corpus):
    '''
    This function searchs the posting list of the term in the dictionary.
    '''
    dictionary = createDictionary(corpus)
    if term in dictionary:              # if the term is in the dictionary
        for key in dictionary:          # for each key of the dictionary
            if key == term:             # if the key is equal to the term
                return dictionary[key]  # return the posting list of the term searched

def checkIfExistTerm(term, corpus):
    '''
    This function checks if a term is in the dictionary.
    '''
    flag = True
    dictionary = createDictionary(corpus)
    if term in dictionary:
        flag = True
    else:
        flag = False
    
    return flag

def andOperator(p1,p2):
    set1 = set(p1)
    set2 = set(p2)
    result =  set1.intersection(set2)
    return result

def orOperator(p1,p2):
    set1 = set(p1)
    set2 = set(p2)
    result = set1.union(set2)
    return result 

def notOperator(p1,p2):
    set1 = set(p1)
    set2 = set(p2)
    result = set1.difference(set2)
    return result

def andOROperator(p1,p2,p3):
    resultOR = list(orOperator(p2,p3))
    result = andOperator(p1,resultOR)
    return result

def andNotOperator(p1,p2,p3):
    resultAnd = list(andOperator(p1,p2))
    result = notOperator(resultAnd, p3)
    return result

def orNotOperator(p1,p2,p3):
    resultOR = list(orOperator(p1,p2))
    result = notOperator(resultOR, p3)
    return result

def notAndOrOperator(p1,p2,p3):
    resultOR = list(orOperator(p2,p3))
    result = notOperator(p1,resultOR)
    return result

def chooseOption1or2or3(option, corpus):
    '''
    This function is for the first three options of the menu, because 
    they only receive two terms. Firts ask for the two terms, then 
    checks if both terms are in the dictionary. If both are in the 
    dictionary, then search the posting list for both and depending 
    of the option chose, it do a boolean operator. If none of the 
    terms or if one of the terms is not in the dictionary, then it 
    print the term that is not in it.
    '''
    try:
        st.subheader('Escriba el primer término')
        term1 = st.text_input('', 'experimental')
    except:
        term1 = 'experimental'
    
    try:
        st.subheader('Escriba el segundo término')
        term2 = st.text_input('', 'potential')
    except:
        term2 = 'potential'

    if st.button('Aceptar'):
        flag1 = checkIfExistTerm(term1, corpus)
        flag2 = checkIfExistTerm(term2, corpus)

        if flag1 == True and flag2 == True:
            postingList1 = searchTerms(term1, corpus)
            postingList2 = searchTerms(term2, corpus)
            if option == '1':
                result = andOperator(postingList1, postingList2)
                for doc in result:
                    st.write(f'Documento # {doc+1}')
            elif option == '2':
                result = orOperator(postingList1, postingList2)
                for doc in result:
                    st.write(f'Documento # {doc+1}')
            elif option == '3':
                result = notOperator(postingList1, postingList2)
                for doc in result:
                    st.write(f'Documento # {doc+1}')
        elif flag1 == True and flag2 == False:
            st.error(f'El término {term2} no está en el diccionario')
        elif flag1 == False and flag2 == True:
            st.error(f'El término {term1} no está en el diccionario')
        else:
            st.error('Los términos no están en el diccionario')
    else:
        pass

def chooseOption4to7(option, corpus):
    '''
    This function is like the "chooseOption1or2or3()" function but 
    with three terms.
    '''
    try:
        st.subheader('Escriba el primer término')
        term1 = st.text_input(' ', 'experimental')
    except:
        term1 = 'experimental'

    try:
        st.subheader('Escriba el segundo término')
        term2 = st.text_input(' ', 'potential')
    except:
        term2 = 'potential'

    try:
        st.subheader('Escriba el tercer término')
        term3 = st.text_input(' ', 'study')
    except:
        term3 = 'study'

    if st.button('Aceptar'):
        flag1 = checkIfExistTerm(term1, corpus)
        flag2 = checkIfExistTerm(term2, corpus)
        flag3 = checkIfExistTerm(term3, corpus)

        if flag1 == True and flag2 == True and flag3 == True:
            postingList1 = searchTerms(term1, corpus)
            postingList2 = searchTerms(term2, corpus)
            postingList3 = searchTerms(term3, corpus)
            if option == '4':
                result = andOROperator(postingList1,postingList2,postingList3)
                for doc in result:
                    st.write(f'Documento # {doc+1}')
            elif option == '5':
                result = andNotOperator(postingList1, postingList2, postingList3)
                for doc in result:
                    st.write(f'Documento # {doc+1}')
            elif option == '6':
                result = orNotOperator(postingList1, postingList2, postingList3)
                for doc in result:
                    st.write(f'Documento # {doc+1}')
            elif option == '7':
                result = notAndOrOperator(postingList1, postingList2, postingList3)
                for doc in result:
                    st.write(f'Documento # {doc+1}')
        elif flag1 == True and flag2 == False and flag3 == True:
            st.error(f'El término {term2} no está en el diccionario')
        elif flag1 == False and flag2 == True and flag3 == True:
            st.error(f'El término {term1} no está en el diccionario')
        elif flag1 == True and flag2 == True and flag3 == False:
            st.error(f'El término {term3} no está en el diccionario')
        elif flag1 == True and flag2 == False and flag3 == False:
            st.error(f'Los términos {term2} y {term3} no están en el diccionario')
        elif flag1 == False and flag2 == True and flag3 == False:
            st.error(f'Los términos {term1} y {term3} no están en el diccionario')
        elif flag1 == False and flag2 == False and flag3 == True:
            st.error(f'Los términos {term1} y {term2} no están en el diccionario')
        else:
            st.error('Los términos no están en el diccionario')
    else:
        pass

def createMenuForUser(corpus):
    '''
    This function creates the menu for the user, so he/she can 
    choose a type of boolean query.
    '''
    st.header('Escoja el tipo de consulta booleana deseada')
    status = st.radio('', ('term1 AND term2', 'term1 OR term2', 
        'term1 AND NOT term2', 'term1 AND (term2 OR term3)', 
            '(term1 AND term2) AND NOT term3', 
                '(term1 OR term2) AND NOT (term3)', 
                    '(term1) AND NOT (term2 OR term3)'))

    if status == 'term1 AND term2':
        chooseOption1or2or3('1', corpus)
    elif status == 'term1 OR term2':
        chooseOption1or2or3('2', corpus)
    elif status == 'term1 AND NOT term2':
        chooseOption1or2or3('3', corpus)
    elif status == 'term1 AND (term2 OR term3)':
        chooseOption4to7('4', corpus)
    elif status == '(term1 AND term2) AND NOT term3':
        chooseOption4to7('5', corpus)
    elif status == '(term1 OR term2) AND NOT (term3)':
        chooseOption4to7('6', corpus)
    elif status == '(term1) AND NOT (term2 OR term3)':
        chooseOption4to7('7', corpus)

def booleanModel(corpus):
    createMenuForUser(corpus)
