from utils.tokenizer import *

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
