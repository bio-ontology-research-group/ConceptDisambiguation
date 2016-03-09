import glob

from cStringIO import StringIO

import numpy as np
import pandas as pd
from cStringIO import StringIO
from pdfminer.pdfinterp import PDFResourceManager, process_pdf
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams

from sklearn.feature_extraction.text import CountVectorizer

MAX_NUM_DOCUMENTS = 1000

# This function is responsible of extracting the pdf content from files.
def getPdfContent(pdfFile):
    input_ = file(pdfFile, 'rb')
    output = StringIO()
    manager = PDFResourceManager()
    converter = TextConverter(manager, output, laparams=LAParams())
    process_pdf(manager, converter, input_)
    return output.getvalue()

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
def buildCorpusRepresentation(stopwords,corpusList):
    if(corpusList):
        vectorizer = CountVectorizer(lowercase=True,stop_words=stopwords,token_pattern='(?u)\\b[\\w+,-]+\\w+\\b|\\b\\w\\w+\\b')
        for abstractPath in corpusList:
            for counter,document in enumerate(glob.iglob(abstractPath)):
                if ((counter<MAX_NUM_DOCUMENTS) and (document)):
                    try:
                        content = getPdfContent(document)
                        if content:
                            X = vectorizer.fit_transform([content])
                    except:
                        print "Error trying to build corpus for the document: "+document
        word_freq_df = pd.DataFrame({'term': vectorizer.get_feature_names(), 'frequency':np.asarray(X.sum(axis=0)).ravel().tolist()})
        word_freq_df.sort_values(by = 'frequency',ascending = False)
        return(word_freq_df)

# This function builds the feature vector representation for each document. Finally, it join all vector in a matrix.
def buildFeatureMatrixRepresentation(stopwords,corpusRepresentation,abstractPath,outPath):
    #featuresMatrix =[]
    if ((not corpusRepresentation.empty) and (abstractPath)):
        fOutput = open(outPath,"wb")
        vectorizer = CountVectorizer(lowercase=True,stop_words=stopwords,token_pattern='(?u)\\b[\\w+,-]+\\w+\\b|\\b\\w\\w+\\b')
        for counter,document in enumerate(glob.iglob(abstractPath)):
            if (document):
                try:
                    fp = open(document,"r");
                    content = fp.read();
                    fp.close()
                    if content:
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
                except:
                    print "Error trying to build the representation for the document: "+document
        fOutput.close();
    #return(featuresMatrix)

# It returns de feature matrix representation of all the documents. The matrix will contain per each document a vector
# that will contain a feature vector of chemicals, diseases and genes.
#def getFeatureMatrix():
outPath = "../outputs/model_approach3.txt"
stopwords = loadStopWords("../resources/stopwords/stopwords.txt")
corpusList =["../resources/abstracts/chemicals/*.pdf","../resources/abstracts/diseases/*.pdf","../resources/abstracts/genes/*.pdf"]
corpusRepresentation = buildCorpusRepresentation(stopwords,corpusList)
buildFeatureMatrixRepresentation(stopwords,corpusRepresentation,"../resources/training/*.txt",outPath)
#return featuresMatrix

