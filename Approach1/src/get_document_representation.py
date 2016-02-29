import glob

import sys

import itertools

import numpy as np
import pandas as pd


from sklearn.feature_extraction.text import CountVectorizer

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

# This function perfoms the frequency analysis of groups documents. Then, it returnsa DataFrame which contains
# the terms and their frequencies.
def buildCorpusRepresentation(stopwords,abstractPath):
    if(abstractPath):
        corpus=[]
        for document in glob.iglob(abstractPath):
            if(document):
                fp = open(document,"r");
                content = fp.read();
                corpus.append(content)
                fp.close()
        if(len(corpus)>0):
            vectorizer = CountVectorizer(lowercase=True,stop_words=stopwords,token_pattern='(?u)\\b[\\w+,-]+\\w+\\b|\\b\\w\\w+\\b')
            X = vectorizer.fit_transform(corpus);
            word_freq_df = pd.DataFrame({'term': vectorizer.get_feature_names(), 'frequency':np.asarray(X.sum(axis=0)).ravel().tolist()})
            word_freq_df.sort_values(by = 'frequency',ascending = False)
            return(word_freq_df)

# This function builds the feature vector representation for each document. Finally, it join all vector in a matrix.
def buildFeatureMatrixRepresentation(stopwords,corpusRepresentation,abstractPath):
    featuresMatrix =[]
    if ((not corpusRepresentation.empty) and (abstractPath)):
        for document in glob.iglob(abstractPath):
            if(document):
                fp = open(document,"r");
                content = fp.read();
                fp.close()
                vector = [];
                #we split each document into tokens.
                vectorizer = CountVectorizer(lowercase=True,stop_words=stopwords,token_pattern='(?u)\\b[\\w+,-]+\\w+\\b|\\b\\w\\w+\\b')
                #vectorizer = CountVectorizer(lowercase=True,stop_words=stopwords)
                analyser = vectorizer.build_analyzer()
                tokens = analyser(content);
                for word in corpusRepresentation.term:
                    if any(word in s for s in tokens):
                        vector.append(1)
                    else:
                        vector.append(0)
                featuresMatrix.append(vector)
                print tokens
                print vector

    return(featuresMatrix)

# It returns de feature matrix representation of all the documents. The matrix will contain per each document a vector
# that will contain a feature vector of chemicals, diseases and genes.
#def getFeatureMatrix(threshold):

threshold = 500;
documentsPath = "../resources/abstracts/chemicals"
stopwords = loadStopWords("../resources/stopwords/stopwords.txt")
chemicalVector = buildCorpusRepresentation(stopwords,"../resources/abstracts/chemicals/*.txt");
if(chemicalVector.size<threshold):
    slicedChemicalVector = chemicalVector
else:
    slicedChemicalVector = chemicalVector.iloc[:threshold]

diseaseVector = buildCorpusRepresentation(stopwords,"../resources/abstracts/diseases/*.txt");
if(diseaseVector.size<threshold):
  slicedDiseaseVector = diseaseVector
else:
  slicedDiseaseVector = diseaseVector.iloc[:threshold]

genesVector = buildCorpusRepresentation(stopwords,"../resources/abstracts/genes/*.txt")
if(genesVector.size<threshold):
  slicedGenesVector = genesVector
else:
  slicedGenesVector = genesVector[:threshold]

#We concat the three DataFrames.
print "Chemical vector length:"+str(len(slicedChemicalVector))
print "Disease vector length:"+str(len(slicedDiseaseVector))
print "Genes vector length:"+str(len(slicedGenesVector))

corpusRepresentation = [slicedChemicalVector,slicedDiseaseVector,slicedGenesVector]
corpusRepresentation = pd.concat(corpusRepresentation)

print "Concatenation:"+str(len(corpusRepresentation))

featuresMatrix =  buildFeatureMatrixRepresentation(stopwords,corpusRepresentation,"../resources/training/*.txt")
print featuresMatrix
#return featuresMatrix