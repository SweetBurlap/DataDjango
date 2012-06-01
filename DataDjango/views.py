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

def uriViewer(request):
    if request.GET['uri']:
        uri = request.GET['uri']
        g=rdflib.Graph()
        g.parse(uri)
        html="<table>"
        for triple in g:
            html+="<tr>"
            for item in triple:
                html+="<td>%s</td>" % item
            html+="</tr>"
        html+="</table>"
        return HttpResponse(html)
    else:
        return HttpResponse("Hello World")
 
import rdflib



    
