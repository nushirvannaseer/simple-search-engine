import os

from bs4 import BeautifulSoup

def tokenizeHtmlDoc(file):
    soup = BeautifulSoup(file, 'html.parser')
    body_tag = list(soup.body.descendants)
    for index, child in enumerate(body_tag):
        print(index, child)
        input()
    exit()


if __name__ == '__main__':
    try:
        # directory = input("Enter the directory for the html files: ")
        directory = 'corpus'
        
        if os.path.exists(directory):
            list_of_files = os.listdir(directory)
            print(f'Total files in directory: {len(list_of_files)}')
            
            #iterate over all the files in the directory
            for filename in list_of_files:
                with open(os.path.join(directory, filename), 'r') as f:
                    tokenizeHtmlDoc(f)
            
        else:
            pass
    except Exception as e:
        print(e)