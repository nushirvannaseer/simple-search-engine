#library imports
import os
import re

#module imports
from bs4 import BeautifulSoup
from nltk.stem import PorterStemmer
from nltk.tokenize import word_tokenize
from collections import Counter
from ordered_set import OrderedSet

#constants
STOP_WORDS = [ word.strip() for word in open('stoplist.txt', 'r').readlines()]
FILTER_REGEX = re.compile('^[0-9A-Za-z](|[-0-9A-Za-z]{0,61}[0-9A-Za-z])$')

#globals
forward_index={}
total_tokens = OrderedSet()
token_ids = {}

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
    
    #adding new tokens to existing tokens_list
    global total_tokens, token_ids
    total_tokens = total_tokens.union(OrderedSet(stripped))
    
    #create a dictionary with all tokens and their assigned ids
    token_ids = { term: i for i, term in enumerate(total_tokens)}
    
    return stripped

def write_termids_to_file(file):
    writable = ''
    for key, value in token_ids.items():
        writable += f'{value}\t{key}\n'
    file.write(writable)
    
def write_doc_indices_to_file(file):
    writable = ''
    for docid, term_list in forward_index.items():
        for t, freq in term_list:
            writable += f'{docid}\t{t}\t{freq}\n'
    file.write(writable)

#main
if __name__ == '__main__':
    try:
        # directory = input("Enter the directory for the html files: ")
        directory = 'corpus'        
        
        if os.path.exists(directory):
            list_of_files = os.listdir(directory)
            print(f'Total files in directory: {len(list_of_files)}')
            
            docids_file = open('docids.txt', 'w+')
            termids_file = open('termids.txt', 'w+')
            doc_index_file = open('doc_index.txt', 'w+')
            
            #variable that stares docid-docname pairs as a long string
            docids = ''
            
            #iterate over all the files in the directory
            for index, filename in enumerate(list_of_files):

                tokenized = None
                
                with open(os.path.join(directory, filename), 'rb') as f:
                    #gets the tokens in the document
                    tokenized = tokenize_html_doc(f)
                docids += f'{str(index)}\t{filename}\n'
                
                tokenized = sorted(tokenized)
                #create frequency dictionary corresponding to docid
                forward_index[index] = Counter(tokenized)
                
                termids = OrderedSet([token_ids[word] for word in tokenized])
                
                
                forward_index[index] = dict(zip(termids, list(forward_index[index].values())))
                forward_index[index] = sorted(forward_index[index].items(), key = lambda kv: kv[0] )
            
                
                if index%500==0:
                    print(f'index: {index}')
            
            
            docids_file.write(docids)
            write_termids_to_file(termids_file)
            write_doc_indices_to_file(doc_index_file)
            docids_file.close()
            termids_file.close()
            
        else:
            print("Directory does not exist!")
    except Exception as e:
        print(e)