#library imports
import sys

#module imports
from nltk.stem import PorterStemmer

#constants
DOCNAME = "--doc"
TERM = "--term"

def create_document_index(file):
    dict_object = dict()
    lines = file.readlines()
    for line in lines:
        props = line.replace('\n', '').split('\t')
        if int(props[0]) not in dict_object.keys():
            dict_object[int(props[0])] = [(int(props[1]), int(props[2]))]
        else:
            dict_object[int(props[0])].append((int(props[1]), int(props[2])))
    
    return dict_object

def create_docid_dictionary(file):
    dict_object = dict()
    lines = file.readlines()
    for line in lines:
        props = line.replace('\n', '').split('\t')
        dict_object[props[1]] = int(props[0])
    return dict_object

def create_termid_dictionary(file):
    dict_object = dict()
    lines = file.readlines()
    for line in lines:
        props = line.replace('\n', '').split('\t')
        dict_object[props[1]] = int(props[0])
    return dict_object

def create_term_info(file):
    lines = file.readlines()
    dict_object = dict()
    for line in lines:
        props = line.replace('\n', '').split('\t')
        dict_object[int(props[0])] = {
            "offset": int(props[1]),
            "total_occurences": int(props[2]),
            "total_documents": int(props[3]),            
        }
    
    return dict_object
    
def list_doc_info(docname, doc_index, docid_dictionary):
    docid = get_doc_id(docname, docid_dictionary)
    distinct_terms = len(doc_index[docid])
    total_terms = sum(j for _, j in doc_index[docid])
    
    print(f'Listing for document: {docname}\nDOCID: {docid}\nDistinct Terms: {distinct_terms}\nTotal Terms: {total_terms}')
    
def get_term_id(term, termid_dictionary):
    return termid_dictionary[PorterStemmer().stem(term)]

def get_doc_id(docname, docid_dictionary):
    return docid_dictionary[docname]

def list_term_info(term,term_info , termid_dictionary):
    #stem the term
    termid = get_term_id(term, termid_dictionary)
    
    #get term offset, total occ, total docs of term
    offset = term_info[termid]['offset']
    total_occurences = term_info[termid]['total_occurences']
    total_documents = term_info[termid]['total_documents']
    
    print(f'Listing for term: {term}\nTERMID: {termid}\nNumber of documents containing term: {total_documents}\nTotal Term frequency in corpus: {total_occurences}\nInverted list offset: {offset}')

def list_both_info(term, docname, termids, docids, term_info):
    termid = get_term_id(term, termids)
    docid=get_doc_id(docname, docids)
    
    offset = term_info[termid]['offset']
    term_freq_in_doc = 0
    with open('../term_index.txt', 'r') as f:
        f.seek(int(offset))
        line = f.readline().replace('\n', '').split('\t')
        for prop in line:
            prop = prop.split(':')
            if len(prop)>1 and int(prop[0]) == docid:
                term_freq_in_doc = int(prop[1])
                break
    print(f'Inverted list for term: {term}\nIn document: {docname}\nTERMID: {termid}\nDOCID: {docid}\nTerm frequency in document: {term_freq_in_doc}')



if __name__ == '__main__':
    try:
        doc_index = create_document_index(open('../doc_index.txt', 'r'))
        docid_dictionary = create_docid_dictionary(open('../docids.txt', 'r'))
        term_info = create_term_info(open('../term_info.txt', 'r'))
        termid_dictionary = create_termid_dictionary(open('../termids.txt', 'r'))
        
        if len(sys.argv) > 1:
            if len(sys.argv) > 3:
                ip = {}
                for i in range(1, len(sys.argv)-1, 2):
                    ip[sys.argv[i]] = sys.argv[i+1]
                list_both_info(ip[TERM], ip[DOCNAME], termid_dictionary, docid_dictionary, term_info)
                
            elif len(sys.argv) == 3:
                if sys.argv[1]==DOCNAME:
                    list_doc_info(sys.argv[2], doc_index, docid_dictionary)
                elif sys.argv[1]==TERM:
                    list_term_info(sys.argv[2], term_info, termid_dictionary)
                else:
                    raise Exception("Argument format incorrect")
            else:
                raise Exception("Argument format incorrect")
            
        else:
            raise Exception("Argument format incorrect")

        
    except Exception as e:
        print(e)
        
        
# def create_inverted_index(file):
#     lines = file.readlines()
#     dict_object = dict()
#     for line in lines:
#         props = line.replace('\n', '').split('\t')
#         postings = []
#         for i in range(1, len(props)):
#             pair=props[i].split(':')
#             docid=int(pair[0])
#             freq = int(pair[1])
#             postings.append((docid, freq)) 
#         dict_object[int(props[0])] = postings

#     return dict_object