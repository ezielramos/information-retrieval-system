import re

from nltk.stem import PorterStemmer

def tokenize(data):
    '''
    Preprocesses the string given as input. Converts to lower case,
    removes the punctuations and numbers, splits on whitespaces, 
    removes stopwords, performs stemming & removes words with one or 
    two characters length.

    Arguments:
        data {string} -- string to be tokenized

    Returns:
        string -- string of tokens generated
    '''

    stop_list = [ 'i', 'me', 'my', 'myself', 'we', 'our', 'ours', 'ourselves', 
                    'you', "you're", "you've", "you'll", "you'd", 'your', 'yours', 
                    'yourself', 'yourselves', 'he', 'him', 'his', 'himself', 'she', 
                    "she's", 'her', 'hers', 'herself', 'it', "it's", 'its', 'itself', 
                    'they', 'them', 'their', 'theirs', 'themselves', 'what', 'which', 
                    'who', 'whom', 'this', 'that', "that'll", 'these', 'those', 'am', 
                    'is', 'are', 'was', 'were', 'be', 'been', 'being', 'have', 'has', 
                    'had', 'having', 'do', 'does', 'did', 'doing', 'a', 'an', 'the', 
                    'and', 'but', 'if', 'or', 'because', 'as', 'until', 'while', 'of', 
                    'at', 'by', 'for', 'with', 'about', 'against', 'between', 'into', 
                    'through', 'during', 'before', 'after', 'above', 'below', 'to', 
                    'from', 'up', 'down', 'in', 'out', 'on', 'off', 'over', 'under', 
                    'again', 'further', 'then', 'once', 'here', 'there', 'when', 
                    'where', 'why', 'how', 'all', 'any', 'both', 'each', 'few', 'more', 
                    'most', 'other', 'some', 'such', 'no', 'nor', 'not', 'only', 'own', 
                    'same', 'so', 'than', 'too', 'very', 's', 't', 'can', 'will', 'just', 
                    'don', "don't", 'should', "should've", 'now', 'd', 'll', 'm', 'o', 
                    're', 've', 'y', 'ain', 'aren', "aren't", 'couldn', "couldn't", 'didn', 
                    "didn't", 'doesn', "doesn't", 'hadn', "hadn't", 'hasn', "hasn't", 
                    'haven', "haven't", 'isn', "isn't", 'ma', 'mightn', "mightn't", 'mustn', 
                    "mustn't", 'needn', "needn't", 'shan', "shan't", 'shouldn', "shouldn't", 
                    'wasn', "wasn't", 'weren', "weren't", 'won', "won't", 'wouldn', "wouldn't"
                ]

    # initiallizing Porter Stemmer object
    st = PorterStemmer()

    # initializing regex to remove words with one or two characters length
    shortword = re.compile(r'\W*\b\w{1,2}\b')

    # converting to lower case
    lines = data.lower()

    # removing punctuations by using regular expression
    lines = re.sub('[^A-Za-z]+', ' ', lines)

    # splitting on whitespaces to generate tokens
    tokens = lines.split()

    # removing stop words from the tokens
    clean_tokens = [ word for word in tokens if word not in stop_list ]

    # stemming the tokens
    stem_tokens = [ st.stem(word) for word in clean_tokens ]

    # checking for stopwords again
    clean_stem_tokens = [ word for word in stem_tokens if word not in stop_list ]

    # converting list of tokens to string
    clean_stem_tokens = ' '.join(map(str,  clean_stem_tokens))

    # removing tokens with one or two characters length
    clean_stem_tokens = shortword.sub('', clean_stem_tokens)

    return clean_stem_tokens
