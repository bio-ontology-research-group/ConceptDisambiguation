#!/usr/bin/env python

import urllib2
import csv

# Given a spreadhseet that contains a list of PMIDs, the function is capable to download the
# abstract from Pubmed
def downloadAbstracts(spreadsheetPath, outPath):
    cr = csv.reader(open(spreadsheetPath,"rb"))
    for row in cr:
        if row[0]!="pmid":
            pmid = row[0]
            try:
                url = 'http://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=pubmed&id='+pmid+'&rettype=fasta&retmode=text'
                response = urllib2.urlopen(url);
                article = response.read()
                if article:
                    abstract = open(outPath+pmid+".txt", 'w')
                    abstract.write(article)
                    abstract.close();
            except urllib2.HTTPError, e:
                print "Error in trying to download the pmid:"+pmid
            except Exception:
                print "Error in trying to download the pmid:"+pmid
            except:
                print "Error in trying to download the pmid:"+pmid
#downloadAbstracts("../resources/documents/chem_documents.csv","../resources/abstracts/chemicals/")
#downloadAbstracts("../resources/documents/disease_documents.csv","../resources/abstracts/diseases/")
downloadAbstracts("../resources/documents/gene_documents.csv","../resources/abstracts/genes/")




