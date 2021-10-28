#library imports
import sys

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

def list_doc_info(docname, doc_index, docid_dictionary):
    docid = docid_dictionary[docname]
    distinct_terms = len(doc_index[docid])
    total_terms = sum(j for i, j in doc_index[docid])
    
    print(f'Listing for document: {docname}\nDOCID: {docid}\nDistinct Terms: {distinct_terms}\nTotal Terms: {total_terms}')
    

def list_term_info(term):
    pass



if __name__ == '__main__':
    try:
        doc_index = create_document_index(open('../doc_index.txt', 'r'))
        docid_dictionary = create_docid_dictionary(open('../docids.txt', 'r'))
        
        
        if len(sys.argv) > 1:
            if len(sys.argv) > 3:
                pass
            elif len(sys.argv) == 3:
                if sys.argv[1]=="--doc":
                    list_doc_info(sys.argv[2], doc_index, docid_dictionary)
                elif sys.arg[1]=="--term":
                    list_term_info(sys.argv[2])
            else:
                raise Exception("Argument format incorrect")

        
    except Exception as e:
        print(e)
        