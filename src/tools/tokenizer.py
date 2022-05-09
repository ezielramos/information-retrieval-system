from nltk import SnowballStemmer

def read_file(path):
    document = open(path, 'r')
    lines = document.readlines()
    document.close()
    return lines

def remove_special_character(line):
    words_without_spaces = line.split()
    words_without_spaces1 = ' '.join(words_without_spaces)

    words_without_semicolons = words_without_spaces1.split(';')
    words_without_semicolons1 = ' '.join(words_without_semicolons)
    
    words_without_colons = words_without_semicolons1.split(':')
    words_without_colons1 = ' '.join(words_without_colons)
    
    words_without_commas = words_without_colons1.split(',')
    words_without_commas1 = ' '.join(words_without_commas)
    
    words_without_dots = words_without_commas1.split('.')
    words_without_dots1 = ' '.join(words_without_dots)

    words_without_div = words_without_dots1.split('/')
    words_without_div1 = ' '.join(words_without_div)

    words_without_minus = words_without_div1.split('-')

    return words_without_minus

def tokenize(lines):

    maximum = 0
    documents_maximum = []
    documents_count = 0
    documents_words = {}
    documents_words_aux = {}
    documents_list = []

    english_stemmer = SnowballStemmer('english')
    stopwords = [ 'i', 'me', 'my', 'myself', 'we', 'our', 'ours', 'ourselves', 
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

    for line in lines:
        if '.I' in line:
            if len(documents_words_aux) != 0:
                documents_maximum.append(maximum)
                maximum = 0
                documents_list.append((documents_count, documents_words_aux.copy()))
                documents_words_aux.clear()
            documents_count += 1
        if '.I' in line or '.T' in line or '.A' in line or '.B' in line or '.W' in line:
            continue
        
        tokens = remove_special_character(line.lower())

        for token in tokens:
            words = token.split(' ')
            words = [ english_stemmer.stem(token) for token in words ]

            for word in words:
                if word in stopwords or len(word) <= 3 or (not word.isalpha()):
                    continue
                
                if word in documents_words:
                    documents_words[word] += 1
                else:
                    documents_words[word] = 1

                if word in documents_words_aux:
                    documents_words_aux[word] += 1
                    maximum = max(maximum, documents_words_aux[word])
                else:
                    documents_words_aux[word] = 1
                    maximum = max(maximum, documents_words_aux[word])
    
    documents_maximum.append(maximum)
    documents_list.append((documents_count, documents_words_aux.copy()))

    return documents_words, documents_list, documents_count, documents_maximum
