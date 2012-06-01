import rdflib
uri = "http://www.w3.org/People/Berners-Lee/card.rdf" #timbls foaf
g=rdflib.Graph()
g.parse(uri)
for triple in g:
    print "TRIPLE"
    for item in triple:
        print item
