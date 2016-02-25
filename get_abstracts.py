import urllib2



lines = [line.rstrip('\n') for line in open('inputFile.txt')] 
lines = set(lines)
print len(lines)
FlopoDic = {}
for line in lines:
    words = line.split(': ')
    response = urllib2.urlopen('http://api.gbif.org/v1/species/match?verbose=true&kingdom=Plantae&name='+words[1])
    webpage = response.read()


