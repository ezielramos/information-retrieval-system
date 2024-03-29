import os
import json
import math as m
import numpy as np
import pandas as pd
import streamlit as st

from collections import Counter

from utils.tokenizer import *
from utils.get_name_file import *
from utils.get_standard_str import *

def cisi_app():

    # declaring variables for file path
    in_path = '../collections/cisi/cisi-all.json'
    out_path = '../collections/cisi/preprocessed_corpus'

    # declaring variables for query_path files
    query_path = '../collections/cisi/cisi-qry.json'
    preprocess_query_path = '../collections/cisi/preprocessed_queries.txt'

    # declaring variable for file with query_path relevance values
    relevance = '../collections/cisi/relevance.txt'

    # checking if the preprocessed docs folder exists already
    if not os.path.isdir(out_path):
        os.mkdir(out_path)

    count = 1

    with open(in_path) as file:

        data = json.load(file)

        for i in data:
            
            # generate filenames
            name_file = get_name_file(count)
            outfilepath = f'{out_path}/cisi{name_file}'

            with open(outfilepath, 'w') as outfile:

                title = data[i]['title']
                text = data[i]['text']
                author = data[i]['author']
                title_tokens = tokenize(title)
                text_tokens = tokenize(text)
                author_tokens = tokenize(author)
                outfile.write(f'{title_tokens} {author_tokens} {text_tokens}')
                count += 1

            outfile.close()

    file.close()

    # preprocessing the queries.txt file
    q = open(query_path)

    # opening new file to write preprocessed tokens into
    new_q = open(preprocess_query_path, 'w')

    # read each line of file seperately
    text = json.load(q)

    for i in text:
        
        a = text[i]['text']
        new_q.write(f'{a}\n')

    q.close()
    new_q.close()

    # getting all filenames from the docs folder
    filenames = os.listdir(out_path)

    # generate a single list of all preprocessed docs
    all_docs = []

    for fname in filenames:
        outfilepath = out_path + '/' + fname
        with open(outfilepath) as file:
            fileData = file.read()
            
            # append file data to the list
            all_docs.append(fileData)
        file.close()

    # total number of documents is 1400
    count_docs = len(all_docs)

    # create a dictionary of key-value pairs where tokens are keys and their occurence in the corpus the value
    frecuencies = {}

    for i in range(count_docs):
        tokens = all_docs[i].split()
        for w in tokens:
            try:
                # add token as key and doc number as value is chained
                frecuencies[w].add(i)
            except:
                # to handle when a new token is encountered
                frecuencies[w] = {i}

    for i in frecuencies:
        # convert to number of occurences of the token from list of documents where token occurs
        frecuencies[i] = len(frecuencies[i])

    # count number of unique words in the corpus
    vocab_size = len(frecuencies)

    # create vocabulary list of all unique words
    vocab = [term for term in frecuencies]

    doc = 0

    # creating dictionary to store tf-idf values for each term in the vocabulary
    tf_idf = {}

    for i in range(count_docs):
        
        tokens = all_docs[i].split()
        
        # counter object to efficiently count number of occurence of a term in a particular document
        counter = Counter(tokens)
        words_count = len(tokens)
        
        for token in np.unique(tokens):
            
            # counting occurence of term in object using counter object
            tf = counter[token] / words_count
            # retrieving df values from frecuencies dictionary
            df = frecuencies[token] if token in vocab else 0
            
            # adding 1 to numerator & denominator to avoid divide by 0 error
            idf = np.log((count_docs + 1) / (df + 1))
            
            tf_idf[doc, token] = tf * idf

        doc += 1

    # initializing empty vector of vocabulary size
    D = np.zeros((count_docs, vocab_size))

    # creating vector of tf-idf values
    for i in tf_idf:
        ind = vocab.index(i[1])
        D[i[0]][ind] = tf_idf[i]

    def gen_vector(tokens):
        '''
        To create a vector (with repsect to the vocabulary) of the tokens 
        passed as input.
        
        Arguments:
            tokens {list} -- list of tokens to be converted.
        
        Returns:
            numpy.ndarray -- vector of tokens.
        '''
        Q = np.zeros((len(vocab)))
        
        counter = Counter(tokens)
        words_count = len(tokens)

        for token in np.unique(tokens):
            
            tf = counter[token]/words_count
            df = frecuencies[token] if token in vocab else 0
            idf = m.log((count_docs + 1) / (df + 1))

            try:
                ind = vocab.index(token)
                Q[ind] = tf * idf
            except:
                pass
        return Q

    def cosine_sim(x, y):
        '''To calculate cosine similarity between 2 vectors.
        
        Arguments:
            x {numpy.ndarray} -- vector 1
            y {numpy.ndarray} -- vector 2
        
        Returns:
            numpy.float64 -- cosine similarity between vector 1 & vector 2
        '''
        if np.linalg.norm(x) * np.linalg.norm(y) == 0:
            cos_sim = 0
        else:
            cos_sim = np.dot(x, y) / (np.linalg.norm(x) * np.linalg.norm(y))
        
        return cos_sim

    def cosine_similarity(k, query_path):
        '''
        To determine a ranked list of top k documents in descending 
        order of their cosine similarity with the query_path.
        
        Arguments:
            k {integer} -- top k documents to retrieve from 
            query_path {string} -- query_path whose cosine similarity 
                                   is to be computed with the corpus.
        
        Returns:
            numpy.ndarray -- list of top k cosine similarities between 
                             query_path and corpus of documents.
        '''

        tokens = query_path.split()
        d_cosines = []
        
        # vectorize the input query_path tokens
        query_vector = gen_vector(tokens)
        
        for d in D:
            d_cosines.append(cosine_sim(query_vector, d))
            
        if k == 0:
            # k=0 to retrieve all documents in descending order
            out = np.array(d_cosines).argsort()[::-1]
            
        else:
            # to retrieve the top k documents in descending order    
            out = np.array(d_cosines).argsort()[-k:][::-1]
        
        return out

    # list of all queries from preprocessed queries file
    query_file = open(preprocess_query_path, 'r')
    queries = query_file.readlines()
    query_file.close()

    def list_of_docs(k):
        '''
        To generate a ranked list of k top documents in descending order of 
        their cosine similarity calculated against the queries. Output is a 
        list of (query_path id, document id) pairs. If k=0 is given as input 
        then list of all documnets in descending order is returned.
        
        Arguments:
            k {integer} -- number of top documents to be retrieved.
        
        Returns:
            list -- list of documents in descending order of their cosine 
                    similarity.
        '''
        cos_sims = []
        for i in range(len(queries)):
            cs = [ i, cosine_similarity(k, queries[i]) ]
            cos_sims.append(cs)
            
        return cos_sims

    # to get list of all documents
    no_of_top = 0
    cos_sims = list_of_docs(no_of_top)

    st.subheader('Consultas')

    for query_id,documents_id in cos_sims:
        docs = []
        for idx,doc in enumerate(documents_id):
            if idx <= 9:
                docs.append(doc)
        st.write(f'Consulta # {get_standard_str(query_id + 1)} = {docs}')

    # retrieving relevance values from relevance.txt
    colnames = [ 'query_path', 'relevance' ]
    rel = pd.read_csv(relevance, delim_whitespace=True, names=colnames, header=None)

    # list of relevant document numbers for a document
    rel_list = []

    # list of list of relevant document numbers for all documents
    query_rel = []
    for i in range(1, 113):
        rel_list = rel[rel['query_path'] == i]['relevance'].to_list()
        
        # append list rel_list to list of list query_list
        query_rel.append(rel_list)

    def intersection(lst1, lst2): 
        '''To count number of common items between 2 lists
        
        Arguments:
            lst1 {list} -- list 1
            lst2 {list} -- list 2
        
        Returns:
            integer -- number of common items between list 1 & list 2 
        '''
        lst3 = [ value for value in lst1 if value in lst2 ]
        return len(lst3) 

    top = [ 50, 100 ]

    def calculate_recall(k):
        '''
        To generate list of recall values for each query_path for given 
        value of k.
        
        Arguments:
            k {integer} -- number of top documents to be retrieved.
        
        Returns:
            list -- list of recall values for each query_path.
        '''
        
        recall = []
        for i in range(len(queries)):

            # number of relevant documents retrieved
            a = intersection(list_of_docs(k)[i][1].tolist(), query_rel[i])

            # total number of relevant documents
            b = len(query_rel[i])
            r = a / b
            recall.append(r)
        return recall

    def calculate_precision(k):
        '''
        To generate list of precision values for each query_path for 
        given value of k.
        
        Arguments:
            k {[type]} -- number of top documents to be retrieved.
        
        Returns:
            list -- list of precision values for each query_path.
        '''
        precision = []
        for i in range(len(queries)):
            
            # number of relevant documents retrieved
            a = intersection(list_of_docs(k)[i][1].tolist(), query_rel[i])
            
            # total number of documents retrieved
            b = k
            p = a / b
            precision.append(p)
        return precision

    def caculate_medida_f(precision, recall, beta=1):
        f = []

        for i in range(len(precision)):
            if precision[i] == 0 or recall[i] == 0:
                f.append(0.0)
            else:
                f.append( ( 1 + (beta * beta) ) / ( ( 1 / precision[i] ) + ( 1 / recall[i] ) ) )
        
        return f

    for t in top:
        p,r = 0,0
        
        st.subheader(f'Primeros {t} documentos de la lista del ranking')
        
        p = calculate_precision(t)
        r = calculate_recall(t)
        f = caculate_medida_f(p, r)

        for i in range(len(queries)):
            st.write(f'Consulta # {get_standard_str(i + 1)} => Precisión : {round(p[i], 3)} , Recobrado : {round(r[i], 3)} , Medida F1 : {round(f[i], 3)}')
        
        st.write(f'Promedio Precisión: {round(np.mean(p), 4)}')
        st.write(f'Promedio Recobrado: {round(np.mean(r), 4)}')
        st.write(f'Promedio Medida F1: {round(np.mean(f), 4)}')
