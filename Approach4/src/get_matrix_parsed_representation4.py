import glob
import string

import numpy as np
import pandas as pd

from sklearn.feature_extraction.text import CountVectorizer

MAX_NUM_ABSTRACTS=13000

def parseContent(lines):
    copy=""
    # to avoid the first /n
    for index in range(1,len(lines)):
        aux=""
        if(lines[index]!='\n'):
            line = lines[index].lower()
            copy += "".join(c for c in line if c not in ('.',',',':',';','\'','"','/','%','(',')','[',']','\n'))
        else:
            copy+=lines[index]
    copy = copy.split('\n');
    return(copy)
# This function perfoms the frequency analysis of groups documents. Then, it returnsa DataFrame which contains
# the terms and their frequencies.
def buildCorpusRepresentation(corpusList,outPath):
    if(corpusList):
        fOutput = open(outPath,"wb")
        counter =0;
        for abstractPath in corpusList:
            for document in glob.iglob(abstractPath):
                if ((counter<MAX_NUM_ABSTRACTS) and (document)):
                    print document
                    fp = open(document,"r");
                    lines = fp.readlines()
                    content = parseContent(lines)
                    if(len(content)>3):
                        title=content[1];
                        abstract=""
                        abstractIndex = 3;
                        if(content[3].startswith("author information")):
                            abstractIndex = 4
                        if((not content[abstractIndex].startswith("pmcid:")) or (not content[abstractIndex].startswith("pmid:"))):
                            for index in range(abstractIndex,len(content)):
                                abstract+=content[index]
                        fOutput.write("".join(title+" "+abstract+"\n"))
                        counter= counter+1
        fOutput.close()
outPath = "../outputs/model_matrix_chemicals_4.txt"
corpusList =["../resources/abstracts/chemicals/*.txt"]
corpusRepresentation = buildCorpusRepresentation(corpusList,outPath)

outPath = "../outputs/model_matrix_diseases_4.txt"
corpusList=["../resources/abstracts/diseases/*.txt"]
corpusRepresentation = buildCorpusRepresentation(corpusList,outPath)

outPath = "../outputs/model_matrix_genes_4.txt"
corpusList=["../resources/abstracts/genes/*.txt"]
corpusRepresentation = buildCorpusRepresentation(corpusList,outPath)




