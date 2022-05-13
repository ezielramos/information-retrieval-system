import os
import math as m
import numpy as np
import pandas as pd

from bs4 import BeautifulSoup
from collections import Counter

from utils.tokenizer import *
from utils.get_standard_str import *

def extract_tokens(beautSoup, tag):
    '''
    Extract tokens of the text between a specific SGML <tag>. The function
    calls tokenize() function to generate tokens from the text.

    Arguments:
        beautSoup {bs4.BeautifulSoup} -- soup bs object formed using text of a file
        tag {string} -- target SGML <tag>

    Returns:
        string -- string of tokens extracted from text between the target SGML <tag>
    '''

    # extract text of a particular SGML <tag>
    text_data = beautSoup.findAll(tag)

    # converting to string
    text_data = ''.join(map(str, text_data))
    # remove the SGML <tag> from text
    text_data = text_data.replace(tag, '')

    # calling function to generate tokens from text
    text_data = tokenize(text_data)

    return text_data

def cranfield():

    # declaring variables for file path
    in_path = '../collections/cranfield/corpus'
    out_path = '../collections/cranfield/preprocessed_corpus'

    # declaring variables for query_path files
    query_path = '../collections/cranfield/queries.txt'
    preprocess_query_path = '../collections/cranfield/preprocessed_queries.txt'

    # declaring variable for file with query_path relevance values
    relevance = '../collections/cranfield/relevance.txt'

    # checking if the preprocessed docs folder exists already
    if not os.path.isdir(out_path):
        os.mkdir(out_path)

    # getting all filenames from the docs folder
    filenames = os.listdir(in_path)  # To generate file path

    for fname in filenames:

        # generate filenames
        infilepath = in_path + '/' + fname
        outfilepath = out_path + '/' + fname

        with open(infilepath) as infile:

            with open(outfilepath, 'w') as outfile:

                # read all text in a file
                fileData = infile.read()

                # creating BeautifulSoup object to extract text between SGML tags
                soup = BeautifulSoup(fileData, features='lxml')

                # extract tokens for <title>
                title = extract_tokens(soup, 'title')

                # extract tokens for <text>
                text = extract_tokens(soup, 'text')

                # write tokens for <title> into new file
                outfile.write(title)
                outfile.write(' ')

                # write tokens for <text> into new file
                outfile.write(text)

            outfile.close()

        infile.close()

    # preprocessing the queries.txt file
    q = open(query_path)

    # opening new file to write preprocessed tokens into
    new_q = open(preprocess_query_path, 'w')

    # read each line of file seperately
    text = q.readlines()
    for line in text:
        
        # if condition to avoid newline character in the end of file
        if(line != text[-1]):
            query_tokens = tokenize(line)
            new_q.write(query_tokens + '\n')
        else:
            query_tokens = tokenize(line)
            new_q.write(query_tokens)

    q.close()
    new_q.close()

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
        '''
        To calculate cosine similarity between 2 vectors.
        
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

    print()
    for i in cos_sims:
        query_id,documents_id = i
        print(f'Consulta # {get_standard_str(query_id + 1)} = [', end=' ')
        for idx,doc in enumerate(documents_id):
            if idx <= 9:
                if idx < 9:
                    print(f'Doc {doc},', end=' ')
                else:
                    print(f'Doc {doc} ]', end=' ')
        print()

    # retrieving relevance values from relevance.txt
    colnames = [ 'query_path', 'relevance' ]
    rel = pd.read_csv(relevance, delim_whitespace=True, names=colnames, header=None)

    # list of relevant document numbers for a document
    rel_list = []

    # list of list of relevant document numbers for all documents
    query_rel = []
    for i in range(1, 11):
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
        lst3 = [value for value in lst1 if value in lst2] 
        return len(lst3) 

    top = [ 10, 50, 100 ]

    # for top 100 docs
    no_of_top = top[2]

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

    # for top 100 docs
    calculate_recall(no_of_top)

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

    # for top 100 docs
    calculate_precision(no_of_top)

    for t in top:
        p,r = 0,0
        
        print(f'\nPrimeros {t} documentos de la lista del ranking\n')
        
        p = calculate_precision(t)
        r = calculate_recall(t)
        for i in range(len(queries)):
            print(f'Consulta # {get_standard_str(i + 1)} \t Precisión : {p[i]} \t Recobrado : {r[i]}')
        
        print(f'\nPromedio Precisión: {np.mean(p)}')
        print(f'Promedio Recobrado: {np.mean(r)}\n')
