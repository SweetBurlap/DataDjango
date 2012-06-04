'''
Created on 1 Jun 2012

@author: Paul

takes a uri query string and displays everything at the corresponding url as a table
this is intentionally a very simple method and will be elaborated on

TODO 
templating rather than string concatenation
Error handling
'''
from django.http import HttpResponse
from django.template import Template, Context

import rdflib
import rdfextras
rdfextras.registerplugins() # so we can Graph.parse()

def uriViewer(request):
    if request.GET.get('uri'):
        uri = request.GET['uri']
        g=rdflib.Graph()
        g.parse(uri)
        results = g.query("""
                SELECT ?p ?o
                WHERE {
                <%s> ?p ?o.
                }
                ORDER BY (?p)
                """ % uri)
        labels = g.query("""
                SELECT ?label
                WHERE {
                <%s> <http://www.w3.org/2000/01/rdf-schema#label> ?label.
                }
                """ %uri)
        label=""
        for label in labels:
            label = str(label[0])
        table = sparqlResultsTable(results)
        pageTemplate = Template("""
        <html>
        <head>
        <title>Data Django - Semantic Web Viewer / Editor</title>
        </head>
        <body>
        <h1>{{h1}}<h1>
        {{body|safe}}
        </body>
        </html>
        """) #I'm sure the safe tag will allow all kind of vulnerabiltiies (consider and antiscript safe one)
        pageContent = Context({"body": table, "h1": label})
        html=pageTemplate.render(pageContent)
        return HttpResponse(html)
    else:
        return index(request) ### if anything goes wrong, go to our index page
        
def index(request):
    return HttpResponse("Hello World")
        
def sparqlResultsTable(results):
##String Concatenating a Simple Table
#    html="<table>"
#    for answer_set in results:
#        html+="<tr>"
#        for item in answer_set:
#            html+="<td>%s</td>" % item
#        html+="</tr>"
#    html+="</table>"
#    
##Templating a Simple Table
#    tableTemplate = Template("""
#    <table>
#    <th><td>Predicate</td><td>Object</td></th>
#    {{rows}}
#    </table>
#    """)
#    
#    rowTemplate = Template("""
#    <tr>{{Cells}}</tr>
#    """)
#    
#    cellTemplate
#    
##Concatenating a Rowspan Table
#    #populate a dictionary of lists - the defaultdict means that we don't have to test for empties
#    from collections import defaultdict
#    dictionary = defaultdict(list)
#    for triple in results:
#        dictionary[str(triple[0])].append(str(triple[1]))
#    htmlresult = """
#    <table>
#    <thead>
#    <tr><th>Predicate</th><th>Object</th></tr>
#    </thead>
#    <tbody>
#    """
#    
#    for k, v in dictionary.iteritems():
#        htmlresult += """<tr><td rowspan="%s">%s</td>""" % (len(v), k,)
#        for item in v[:1]: #the first case is different as we have already started our row
#            htmlresult += "<td>%s</td></tr>" %item
#        for item in v[1:]:
#            htmlresult += "<tr><td>%s</td></tr>" %item
#    
#    htmlresult += """
#    </tbody>
#    <table>
#    """
    
    #Templating a Rowspan Table
    
    table = Template("""{% autoescape off %}
    <table>
    <thead><th>Predicate</th><th>Object</th></thead>
    <tbody>{{tbody}}</tbody>
    </table>
    {% endautoescape %}""")
    tbody = ""
    merged_row = Template("""{% autoescape off %}<tr><td rowspan="{{rowspan}}">{{predicate}}</td><td>{{first_object}}</td>{{other_object_cells}}</tr>{% endautoescape %}""")
    object_only_row = Template("""{% autoescape off %}<tr><td>{{object}}</td></tr>{% endautoescape %}""")
        
    previous_line = ("","",)
    c=Context({})

    rowspan = 0
    other_object_cells = ""
    predicate_display = ""
    first_object = ""

    for line in results:
        if line[0] != previous_line[0]:#if the predicate's new
            if previous_line: #if the previous line has been set its not our first pass
                c = Context({"rowspan": rowspan, "predicate": predicate_display, "first_object": first_object, "other_object_cells": other_object_cells})#render the merged row
                tbody+=merged_row.render(c) #append the merged row to the tbody
            rowspan = 1
            other_object_cells = ""
            predicate_display = display_URI(line[0])
            first_object = display_URI(line[1])
    
        else: #old predicate
            rowspan += 1 #increment rowspan
            next_object = display_URI(line[1])
            object_only_context = Context({"object": next_object})
            other_object_cells+=object_only_row.render(object_only_context) #add object only row
            
        previous_line = line #store the current line as previous line (so we can compare predicates)
        
    tableContext = Context({"tbody": tbody})
    html = table.render(tableContext)
    
    return html

def display_URI(uri):
    linkTemplate = Template("""<a href="?uri={{href|urlencode}}">{{linkText}}</a>""")
    if type(uri)== rdflib.term.URIRef:
        label = get_label(uri)
        display = linkTemplate.render(Context({"href": uri, "linkText": label})) #we need to go rdfs:label hunting, try local store, try dereferencing
    else:
        display = uri
    return display

def get_label(uri):
    g=rdflib.Graph()
    if g.parse(uri): #could change this to sparql wrapper to use only a single endpoint
        results = g.query("""
        SELECT ?label
        WHERE {
        <%s> <http://www.w3.org/2000/01/rdf-schema#label> ?label.
        }
        """ %uri)
        if results:
            result_list = []
            for result in results:
                result_list.append(result[0])
            return result_list[0]
    else:
        return uri
        
        
        
if __name__ == "__main__": #for testign purposes
    uri = "http://www.w3.org/People/Berners-Lee/card#i"


    
