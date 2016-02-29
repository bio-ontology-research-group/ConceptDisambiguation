#!/usr/bin/env python

import csv

# IDs of the dictionaries
# 51;"Chemical Entities of Biological Interest (ChEBI)"
# 46;"Archaea Genes (EntrezGene)"
# 47;"Bacteria Genes (EntrezGene)"
# 49;"Viruses Genes (EntrezGene)"
# 48;"Fungi Genes (EntrezGene)"
# 2;"Human Genes and Proteins (EntrezGene)"
# 52;"Disease Ontology (DO)"

# Organization of the list of words.
# id_term;"id_concept";"name_term";"fk_id_dictionary";"active_term"
cr = csv.reader(open("../resources/words/used_terms.csv","rb"))


geneDictionary = open("../resources/dictionaries/genesDictionary.txt", "w")
chemicalDictionary = open("../resources/dictionaries/chemicalDictionary.txt","w")
diseaseDictionary = open("../resources/dictionaries/diseaseDictionary.txt","w")
for row in cr:
    line=""
    for index in row:
        line=line+index
    line = line.replace("\"","")
    line = line.replace("'","")
    properties = line.split(";");
    if properties[0]!="id_term":
        idDictionary = int(properties[len(properties)-2]) #fk_id_dictionary
        if (idDictionary == 46) or (idDictionary ==47) or (idDictionary==48) or (idDictionary==49): #genes
            word = properties[2]
            geneDictionary.write(word+"\n")
        elif(idDictionary == 51): #chemical
            word = properties[2]
            chemicalDictionary.write(word+"\n")
        elif(idDictionary == 52): # disease
            word = properties[2]
            diseaseDictionary.write(word+"\n")

geneDictionary.close()
chemicalDictionary.close()
diseaseDictionary.close()