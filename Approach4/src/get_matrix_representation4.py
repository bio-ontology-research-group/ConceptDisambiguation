import glob
import string

import numpy as np
import pandas as pd

from sklearn.feature_extraction.text import CountVectorizer

MAX_NUM_ABSTRACTS=13000

def checkContent(content):
    # We lowcase content
    content = content.lower()
    # We delete the punctuation symbols
    content = "".join(c for c in content if c not in ('.',',',':',';','\'','"','/','%','(',')','[',']'))
    # We normalise whitespace
    content=' '.join(content.split())
    return(content)
# This function perfoms the frequency analysis of groups documents. Then, it returnsa DataFrame which contains
# the terms and their frequencies.
def buildCorpusRepresentation(corpusList,outPath):
    if(corpusList):
        fOutput = open(outPath,"wb")
        for abstractPath in corpusList:
            for counter,document in enumerate(glob.iglob(abstractPath)):
                if ((counter<MAX_NUM_ABSTRACTS) and (document)):
                    try:
                        fp = open(document,"r");
                        lines = fp.readlines()
                        fp.close()
                        final = [];
                        #We escape the first line, which is empty
                        #We escape the authors
                        for index in range(1,len(lines)):
                            aux = checkContent(lines[index])
                            if len(aux.strip())==0:
                                #We seek in the next text
                                index = index+1
                                break;
                        #We get the title
                        for index in range(index,len(lines)):
                            aux = checkContent(lines[index])
                            if(len(aux.strip()))!=0:
                                final.append(aux)
                            else:
                                index = index + 1
                                break

                        #We scape the authors
                        for index in range(index,len(lines)):
                            aux = checkContent(lines[index])
                            if len(aux.strip())==0:
                                index=index+1
                                break;
                        #We scape the Author Information:
                        for index in range(index,len(lines)):
                            aux = checkContent(lines[index])
                            if len(aux.strip())==0:
                                index=index+1
                                break;
                        #We collect the Abstract.
                        for index in range(index,len(lines)):
                            aux = checkContent(lines[index])
                            if not aux.startswith("pmid") and len(aux.strip())!=0:
                                final.append(aux)

                        fOutput.write(" ".join(final)+"\n")
                    except:
                        print "Error trying to build corpus for the document: "+document
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




