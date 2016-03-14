# Namirud Yegezu 26447410
# Kevin Chen 49859223

import collections
from bs4 import BeautifulSoup
import json
import re
import string
import time
import io
import math
import codecs

def writeIndexToFile(index):
    with codecs.open("tf_idf_test.txt","w","utf-8") as f:
        json.dump(index, f)


def main():
    docIDtoURL = collections.defaultdict()
    inverted_index = collections.defaultdict()
    tf_idf = collections.defaultdict()
    doc_freq = collections.defaultdict()
    words_doc = collections.defaultdict()
    terms = collections.defaultdict()
    
    #declared variables 
    count = 1
    punct = string.punctuation
    allowedChar = string.ascii_letters+string.digits



    #opening json file
    with open('test_files.json') as data_file:    
        data = json.load(data_file)

    regex = re.compile('[^a-zA-Z0-9]')

    numFiles = 0
    nonstop_words = [word.rstrip('\n') for word in open('long_nonstop_words.txt')]

    #parsing thru json file
    try:
        for i in data:
            term_freq = collections.defaultdict()
            fileName = data[i]["file"]
            try:
                ecj_data = io.open("Html/"+fileName,'r',encoding='utf-8').read()
                soup = BeautifulSoup(ecj_data, "html.parser")
            except Exception:
                print("Error")
      
            visible_text = soup.getText()
            visible_text = ''.join(regex.sub(' ', ch) for ch in visible_text)
            wordsInFile = visible_text.split()
            # docID as key, url as value
            docIDtoURL[i] = data[i]["url"]

            # count term frequency
            count = 0
            for word in wordsInFile:
                word = word.lower()
                if len(word) > 1 and word not in nonstop_words:
                    if word in term_freq:
                        term_freq[word] += 1
                    else:
                        term_freq[word] = 1
                    count += 1
            
            # update terms
            for word in term_freq.keys():
                if word in terms:
                    terms[word].append(i)
                else:
                    terms[word] = [i]
            
            # update term in doc 
            for word in term_freq.keys():
                if word in doc_freq:
                    doc_freq[word] += 1
                else:
                    doc_freq[word] = 1
                inverted_index[word] = dict({i:term_freq[word]})
            # doc id with total number of words
            words_doc[i] = count

        for word in inverted_index.keys():
            for docID in inverted_index[word].keys():
                if docID in terms[word]:
                    top = 1.4 * inverted_index[word][docID]
                    bottom = words_doc[docID] * math.log(44535/doc_freq[word])
                    tf_idf[word] = dict({docID:(top/bottom)*100})
                else:
                    top = inverted_index[word][docID]
                    bottom = words_doc[docID] * math.log(44535/doc_freq[word])
                    tf_idf[word] = dict({docID:(top/bottom)*100})


        writeIndexToFile(tf_idf)
        
        
    except KeyboardInterrupt:
        print("--- %s seconds ---" % (time.time() - start_time))
        print(len(newList))
        


if __name__ == "__main__":
    start_time = time.time()
    main()
    print("--- %s seconds ---" % (time.time() - start_time))


