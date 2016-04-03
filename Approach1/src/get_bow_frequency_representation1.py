import glob

import numpy as np
import pandas as pd


from sklearn.feature_extraction.text import CountVectorizer

MAX_NUM_ABSTRACTS=13000
MAX_LENGTH_VECTOR = 1000;

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
def buildCorpusRepresentation(stopwords,abstractPath):
    if(abstractPath):
        vectorizer = CountVectorizer(lowercase=True,stop_words=stopwords,token_pattern='(?u)\\b[\\w+,-]+\\w+\\b|\\b\\w\\w+\\b')
	corpus=[]
        for counter,document in enumerate(glob.iglob(abstractPath)):
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
	    X = vectorizer.fit_transform(corpus)
            word_freq_df = pd.DataFrame({'term': vectorizer.get_feature_names(), 'frequency':np.asarray(X.sum(axis=0)).ravel().tolist()})
            word_freq_df = word_freq_df.sort_values(by = 'frequency',ascending = False)
        return(word_freq_df)

# This function builds the feature vector representation for each document. Finally, it join all vector in a matrix.
def buildFeatureMatrixRepresentation(stopwords,chemicalsVector,diseasesVector,genesVector,corpusList,outPath):
    #featuresMatrix =[]
    if ((not chemicalsVector.empty) and (not diseasesVector.empty) and (not genesVector.empty) and (corpusList)):
        fOutput = open(outPath,"w")
        vectorizer = CountVectorizer(lowercase=True,stop_words=stopwords,token_pattern='(?u)\\b[\\w+,-]+\\w+\\b|\\b\\w\\w+\\b')
        for abstractPath in corpusList:
            for counter,document in enumerate(glob.iglob(abstractPath)):
                if ((counter<MAX_NUM_ABSTRACTS) and (document)):
                    try:
                        fp = open(document,"r");
                        content = fp.read();
                        fp.close()
                        if content:
                            vector = [];
                            #we split each document into tokens.
                            analyser = vectorizer.build_analyzer()
                            tokens = analyser(content);
                            for record in enumerate(chemicalsVector.values):
				freq = record[1][0]
				word = record[1][1]	
                                if word!= " " and any(word in s for s in tokens):
                                    vector.append(freq)
                                else:
                                    vector.append(0)
                            for record in enumerate(diseasesVector.values):
				freq = record[1][0]
				word = record[1][1]
                                if word!= " " and any(word in s for s in tokens):
                                    vector.append(freq)
                                else:
                                    vector.append(0)
                            for record in enumerate(genesVector.values):
				freq = record[1][0]
				word = record[1][1]
                                if word!= " " and any(word in s for s in tokens):
                                    vector.append(freq)
                                else:
                                    vector.append(0)
                            #featuresMatrix.append(vector)
                            fOutput.write(" ".join(str(x) for x in vector)+"\n")
                    except:
                        print "Error trying to build the representation for the document: "+document
        fOutput.close();
    #return(featuresMatrix)

# It returns de feature matrix representation of all the documents. The matrix will contain per each document a vector
# that will contain a feature vector of chemicals, diseases and genes.
#def getFeatureMatrix(threshold):
outPath="../outputs/model_approach_frequency_1_1K.txt"
stopwords = loadStopWords("../resources/stopwords/stopwords.txt")
chemicalsVector = buildCorpusRepresentation(stopwords,"../resources/abstracts/chemicals/*.txt");
# All vectors should have the same lenght, if not we fill up with zeros.

#We divide by 2 because the representation vector contains 2 rows: terms | frequency
if(MAX_LENGTH_VECTOR>(chemicalsVector.size/2)):
    size = (MAX_LENGTH_VECTOR-(chemicalsVector.size/2))
    zeros = pd.DataFrame({'term': [" "]*size , 'frequency':np.zeros(size)})
    slicedChemicalsVector = [chemicalsVector,zeros]
    slicedChemicalsVector = pd.concat(slicedChemicalsVector)
else:
    slicedChemicalsVector = chemicalsVector.iloc[:MAX_LENGTH_VECTOR]

diseasesVector = buildCorpusRepresentation(stopwords,"../resources/abstracts/diseases/*.txt");
if(MAX_LENGTH_VECTOR>(diseasesVector.size/2)):
    size = (MAX_LENGTH_VECTOR-(diseasesVector.size/2))
    zeros = pd.DataFrame({'term': [" "]*size, 'frequency':np.zeros(size)})
    slicedDiseasesVector = [diseasesVector,zeros]
    slicedDiseasesVector = pd.concat(slicedDiseasesVector)
else:
    slicedDiseasesVector = diseasesVector.iloc[:MAX_LENGTH_VECTOR]

genesVector = buildCorpusRepresentation(stopwords,"../resources/abstracts/genes/*.txt")
if(MAX_LENGTH_VECTOR>(genesVector.size/2)):
    size = (MAX_LENGTH_VECTOR-(genesVector.size/2))
    zeros = pd.DataFrame({'term': [" "]*size, 'frequency':np.zeros(size)})
    slicedGenesVector = [genesVector,zeros]
    slicedGenesVector = pd.concat(slicedGenesVector)
else:
    slicedGenesVector = genesVector[:MAX_LENGTH_VECTOR]

#We divide by two in order to consider the quantity of terms.
print "The length of chemicals vector: "+str(slicedChemicalsVector.size/2)
print "The length of diseases vector: "+str(slicedDiseasesVector.size/2)
print "The length of genes vector: "+str(slicedGenesVector.size/2)

#We concat the three DataFrames.
corpusList =["../../../GetAbstracts/resources/abstracts/chemicals/*.txt","../../../GetAbstracts/resources/abstracts/diseases/*.txt","../../../GetAbstracts/resources/abstracts/genes/*.txt"]
buildFeatureMatrixRepresentation(stopwords,slicedChemicalsVector,slicedDiseasesVector,slicedGenesVector,corpusList,outPath)
#return featuresMatrix
