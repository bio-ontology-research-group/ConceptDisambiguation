import groovyx.gpars.GParsPool

// Given a spreadhseet that contains a list of PMIDs, the function is capable to download the

def downloadAbstracts= { spreadsheetPath, outPath ->
    GParsPool.withPool(2) {
        //new File(spreadsheetPath).splitEachLine(",") { fields ->
        List<String> lines = new File(spreadsheetPath).readLines();
        lines.eachParallel { String line ->
            String[] fields = line.split(",");
            if (!fields[0].contains("pmid")) {
                String pmid = fields[0];
                try {
                    File fArticle = new File(outPath + pmid + ".txt");
                    if (!fArticle.exists()) {
                        String url = 'http://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=pubmed&id=' + pmid + '&rettype=fasta&retmode=text'
                        String article = url.toURL().getText()
                        if ((article != null) && (!article.isEmpty())) {
                            BufferedWriter fout = new BufferedWriter(new FileWriter(fArticle));
                            fout.write(article);
                            fout.close()
                            // We try to get the whole document
                            url = 'http://www.ncbi.nlm.nih.gov/pmc/utils/idconv/v1.0/?tool=my_tool&email=my_email@example.com&ids=' + pmid
                            String response = url.toURL().getText();
                            if ((response != null) && (!response.isEmpty())) {
                                pmcids = new XmlSlurper().parseText(response)
                                String pmcid = pmcids.record.@pmcid;
                                if ((pmcid != null) && (!pmcid.isEmpty())) {
                                    url = 'http://www.ncbi.nlm.nih.gov/pmc/utils/oa/oa.fcgi?id=' + pmcid
                                    response = url.toURL().getText();
                                    oaRecords = new XmlSlurper().parseText(response)
                                    records = oaRecords.records.record.link.each { link ->
                                        if (link.@format == "pdf") {
                                            String href = link.@href;
                                            def pdfAbstract = new File(outPath + pmid + ".pdf");
                                            pdfAbstract << new URL(href).openStream()
                                        }
                                    }
                                } else {
                                    println "The pmid:" + pmid + " does not have a document"
                                }
                            }
                        }
                    }
                } catch (Exception e) {
                    print e.getMessage()
                    print "Error in trying to download the pmid:" + pmid
                }
            }
        }
    }
}
def list = [];
Expando chemicals = new Expando()
chemicals.csv="../resources/documents/chem_documents.csv"
chemicals.path="../resources/abstracts/chemicals/"
list.add(chemicals)
Expando diseases = new Expando()
diseases.csv="../resources/documents/disease_documents.csv"
diseases.path="../resources/abstracts/diseases/"
list.add(diseases)
Expando genes = new Expando()
genes.csv="../resources/documents/gene_documents.csv"
genes.path="../resources/abstracts/genes/"
list.add(genes)
GParsPool.withPool {
    list.each { expando ->
        downloadAbstracts(expando.csv, expando.path)
    }
}




