import glob

import numpy as np
import pandas as pd

from sklearn.feature_extraction.text import CountVectorizer

MAX_NUM_ABSTRACTS=13000
MAX_LENGTH_VECTOR = 5000;

# This function is responsible of building the stop words list.
def loadStopWords(dictionaryPath):
    dictionary=[]
    if(dictionaryPath):
        f = open(dictionaryPath, "r")
        dictionary = f.read().splitlines();
        #change into lower all words.
        dictionary = map(str.lower, dictionary)
        #delete duplicates
        dictionary = list(set(dictionary))
    return dictionary

# This function perfoms the frequency analysis of groups documents. Then, it returns DataFrame which contains
# the terms and their frequencies.
def buildCorpusRepresentation(stopwords,corpusList):
    if(corpusList):
        vectorizer = CountVectorizer(lowercase=True,stop_words=stopwords,token_pattern='(?u)\\b[\\w+,-]+\\w+\\b|\\b\\w\\w+\\b')
        corpus=[]
        for abstractPath in corpusList:
            for counter, document in enumerate(glob.iglob(abstractPath)):
                if ((counter<MAX_NUM_ABSTRACTS) and (document)):
                    try:
                        fp = open(document,"r");
                        content = fp.read();
                        fp.close()
                        if content:
                            corpus.append(content)
                    except:
                        print "Error trying to build corpus for the document: "+document
        if corpus:
            X = vectorizer.fit_transform(corpus);
            word_freq_df = pd.DataFrame({'term': vectorizer.get_feature_names(), 'frequency':np.asarray(X.sum(axis=0)).ravel().tolist()})
            word_freq_df = word_freq_df.sort_values(by = 'frequency',ascending = False)
        return(word_freq_df)

# This function builds the feature vector representation for each document. Finally, it join all vector in a matrix.
def buildFeatureMatrixRepresentation(stopwords,corpusRepresentation,corpusList,outPath):
    #featuresMatrix =[]
    if ((not corpusRepresentation.empty) and (corpusList)):
        fOutput = open(outPath,"w")
        vectorizer = CountVectorizer(lowercase=True,stop_words=stopwords,min_df=0,token_pattern='(?u)\\b[\\w+,-]+\\w+\\b|\\b\\w\\w+\\b',
                                     vocabulary=corpusRepresentation.term.tolist())
        fOutput.write(" ".join(x.encode("utf8") for x in corpusRepresentation.term.tolist())+"\n")
        for abstractPath in corpusList:
            for counter,document in enumerate(glob.iglob(abstractPath)):
                if ((counter<MAX_NUM_ABSTRACTS) and (document)):
                    try:
                        fp = open(document,"r");
                        content = fp.read();
                        fp.close()
                        if content:
                            vector = np.zeros(len(vectorizer.vocabulary));
                            X = vectorizer.fit_transform([content])
                            word_freq_df = pd.DataFrame({'term': vectorizer.get_feature_names(), 'frequency':np.asarray(X.sum(axis=0)).ravel().tolist()})
                            fOutput.write(" ".join(str(x) for x in word_freq_df.frequency.tolist())+"\n")
                    except:
                        print "Error trying to build the representation for the document: "+document
        fOutput.close();
    #return(featuresMatrix)

# It returns de feature matrix representation of all the documents. The matrix will contain per each document a vector
# that will contain a feature vector of chemicals, diseases and genes.
#def getFeatureMatrix():
outPath = "../outputs/model_approach_frequency_2.txt"
stopwords = loadStopWords("../resources/stopwords/stopwords.txt")
corpusList =["../resources/abstracts/chemicals/*.txt","../resources/abstracts/diseases/*.txt","../resources/abstracts/genes/*.txt"]
corpusRepresentation = buildCorpusRepresentation(stopwords,corpusList)

if(MAX_LENGTH_VECTOR>(corpusRepresentation.size/2)):
    size = (MAX_LENGTH_VECTOR-(corpusRepresentation.size/2))
    zeros = pd.DataFrame({'term': [" "]*size , 'frequency':np.zeros(size)})
    slicedChemicalsVector = [corpusRepresentation,zeros]
    slicedChemicalsVector = pd.concat(slicedChemicalsVector)
else:
    slicedChemicalsVector = corpusRepresentation.iloc[:MAX_LENGTH_VECTOR]

print "The lenght of the corpus representation is:"+str(len(slicedChemicalsVector))

buildFeatureMatrixRepresentation(stopwords,slicedChemicalsVector,corpusList,outPath)

#buildFeatureMatrixRepresentation(stopwords,corpusRepresentation,"../resources/training/*.txt",outPath)
#return featuresMatrix

