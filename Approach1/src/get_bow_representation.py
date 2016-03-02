import glob

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
        vectorizer = CountVectorizer(lowercase=True,stop_words=stopwords,token_pattern='(?u)\\b[\\w+,-]+\\w+\\b|\\b\\w\\w+\\b')
        for document in glob.iglob(abstractPath):
            if(document):
                fp = open(document,"r");
                content = fp.read();
                fp.close()
                X = vectorizer.fit_transform([content]);
        word_freq_df = pd.DataFrame({'term': vectorizer.get_feature_names(), 'frequency':np.asarray(X.sum(axis=0)).ravel().tolist()})
        word_freq_df.sort_values(by = 'frequency',ascending = False)
        return(word_freq_df)

# This function builds the feature vector representation for each document. Finally, it join all vector in a matrix.
def buildFeatureMatrixRepresentation(stopwords,corpusRepresentation,abstractPath,outPath):
    #featuresMatrix =[]
    if ((not corpusRepresentation.empty) and (abstractPath)):
        fOutput = open(outPath,"w")
        vectorizer = CountVectorizer(lowercase=True,stop_words=stopwords,token_pattern='(?u)\\b[\\w+,-]+\\w+\\b|\\b\\w\\w+\\b')
        for document in glob.iglob(abstractPath):
            if(document):
                fp = open(document,"r");
                content = fp.read();
                fp.close()
                vector = [];
                #we split each document into tokens.
                analyser = vectorizer.build_analyzer()
                tokens = analyser(content);
                for word in corpusRepresentation.term:
                    if any(word in s for s in tokens):
                        vector.append(1)
                    else:
                        vector.append(0)
                #featuresMatrix.append(vector)
                fOutput.write(" ".join(str(x) for x in vector)+"\n")
        fOutput.close();
    #return(featuresMatrix)

# It returns de feature matrix representation of all the documents. The matrix will contain per each document a vector
# that will contain a feature vector of chemicals, diseases and genes.
#def getFeatureMatrix(threshold):
threshold = 500;
outPath="../outputs/model_approach1.txt"
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

buildFeatureMatrixRepresentation(stopwords,corpusRepresentation,"../resources/training/*.txt",outPath)
#return featuresMatrix