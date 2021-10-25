#library imports
import os
import re

#module imports
from bs4 import BeautifulSoup
from nltk.stem import PorterStemmer
from nltk.tokenize import word_tokenize

#constants
STOP_WORDS = [ word.strip() for word in open('stoplist.txt', 'r').readlines()]
FILTER_REGEX = re.compile('^[0-9A-Za-z](|[-0-9A-Za-z]{0,61}[0-9A-Za-z])$')

#functions
def remove_tags(soup):  
    for data in soup(['style', 'script']):
        # Remove tags
        data.decompose()
  
    # return data by retrieving the tag content
    return ' '.join(soup.stripped_strings)

def remove_stop_words(text):
    querywords = text.split()
    return [word for word in querywords if word not in STOP_WORDS]

def apply_stemming(word_list):
    ps = PorterStemmer()
    stemmed_words = []
    for w in word_list:
        if FILTER_REGEX.match(w):
            stemmed_words.append(ps.stem(w))
    return stemmed_words

def tokenize_html_doc(file):
    soup = BeautifulSoup(file, 'html.parser')
    soup_head = soup.head
    soup_body = soup.body
    
    stripped = ''
    
    if soup_head:
        stripped += remove_tags(soup_head) 
    if soup_body:
        stripped += remove_tags(soup_body)
        
    stripped = stripped.replace('  ', '').replace('\n', ' ').replace('\t', ' ').replace('\r', '').replace('.', '').replace(',', '').replace('"', '').replace("'", '')
    
    stripped = stripped.lower()
    #get a list of words without stopwords
    stripped = remove_stop_words(stripped)
    stripped = apply_stemming(stripped)
    return stripped

def write_termids_to_file(termids, file):
    writable = ''
    for index, term in enumerate(termids):
        writable += f'{index}\t{term}\n'
    file.write(writable)


#main
if __name__ == '__main__':
    try:
        # directory = input("Enter the directory for the html files: ")
        directory = 'corpus'
        print(STOP_WORDS)
        
        
        if os.path.exists(directory):
            list_of_files = os.listdir(directory)
            print(f'Total files in directory: {len(list_of_files)}')
            
            docids_file = open('docids.txt', 'w+')
            termids_file = open('termids.txt', 'w+')
            doc_index_file = open('doc_index.txt', 'w+')
            
            docids = ''
            termids = set()
            #iterate over all the files in the directory
            for index, filename in enumerate(list_of_files):
                # print(f'FILENAME: {filename}\n\n\n')
                tokenized = None
                with open(os.path.join(directory, filename), 'rb') as f:
                    tokenized = tokenize_html_doc(f)
                docids += f'{str(index)}\t{filename}\n'
                
                termids = termids.union(set(tokenized))
                if index%500==0:
                    print(f'index: {index}')
                if index == 200:
                    break
            
            docids_file.write(docids)
            write_termids_to_file(termids, termids_file)
            docids_file.close()
            termids_file.close()
            
        else:
            pass
    except Exception as e:
        print(e)