#!/usr/bin/env python

import urllib2
import csv

# Given a spreadhseet that contains a list of PMIDs, the function is capable to download the
# abstract from Pubmed
from xml.dom import minidom


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
                    # We try to get the whole document
                    url ='http://www.ncbi.nlm.nih.gov/pmc/utils/idconv/v1.0/?tool=my_tool&email=my_email@example.com&ids='+pmid
                    response = urllib2.urlopen(url);
                    if response :
                        xmldoc = minidom.parse(response)
                        record = xmldoc.getElementsByTagName('record');
                        if record and record[0].hasAttribute('pmcid') :
                            pmcid = record[0].attributes['pmcid'].value;
                            url='http://www.ncbi.nlm.nih.gov/pmc/utils/oa/oa.fcgi?id='+pmcid
                            response = urllib2.urlopen(url);
                            xmldoc = minidom.parse(response)
                            records=xmldoc.getElementsByTagName('link');
                            for format in records:
                                if(format.attributes['format'].value == "pdf"):
                                    href = format.attributes['href'].value;
                                    response= urllib2.urlopen(href)
                                    pdfAbstract= open(outPath+pmid+".pdf", 'w')
                                    pdfAbstract.write(response.read())
                                    pdfAbstract.close()
                        else:
                            print "The pmid:"+pmid+" does not have a document"
            except urllib2.HTTPError, e:
                print "Error in trying to download the pmid:"+pmid
            except Exception:
                print "Error in trying to download the pmid:"+pmid
            except:
                print "Error in trying to download the pmid:"+pmid
downloadAbstracts("../resources/documents/chem_documents.csv","../resources/abstracts/chemicals/")
downloadAbstracts("../resources/documents/disease_documents.csv","../resources/abstracts/diseases/")
downloadAbstracts("../resources/documents/gene_documents.csv","../resources/abstracts/genes/")


