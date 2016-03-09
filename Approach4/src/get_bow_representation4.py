import glob
import numpy as np
import pandas as pd

from sklearn.feature_extraction.text import CountVectorizer

# This function is responsible of building the stop words list.
def loadStopWords(dictionaryPath):
    dictionary=[]
    if(dictionaryPath):
        try:
            f = open(dictionaryPath, "r")
            dictionary = f.read().splitlines();
            #change into lower all words.
            dictionary = map(str.lower, dictionary)
            #delete duplicates
            dictionary = list(set(dictionary))
        except:
             print "Error trying to load the stopwords"
    return dictionary

# This function perfoms the frequency analysis of groups documents. Then, it returnsa DataFrame which contains
# the terms and their frequencies.
def buildCorpusRepresentation(stopwords,corpusList,outPath):
    if(corpusList):
        fOutput = open(outPath,"wb")
        for abstractPath in corpusList:
            for counter,document in enumerate(glob.iglob(abstractPath)):
                if (document):
                    try:
                        fp = open(document,"r");
                        content = fp.read();
                        fp.close()
                        if content:
                            wordList = content.split();
                            row =[]
                            for word in wordList:
                                if word.lower() not in (stopwords):
                                    row.append(word);
                            fOutput.write(" ".join(str(x) for x in row)+"\n")

                    except:
                        print "Error trying to build corpus for the document: "+document
        fOutput.close()

outPath = "../outputs/model_approach4.txt"
stopwords = loadStopWords("../resources/stopwords/stopwords.txt")
corpusList =["../resources/abstracts/chemicals/*.txt","../resources/abstracts/diseases/*.txt","../resources/abstracts/genes/*.txt"]
corpusRepresentation = buildCorpusRepresentation(stopwords,corpusList,outPath)


