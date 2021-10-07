import logging
from urllib import parse

from requests import Response
from SPARQLWrapper import SPARQLWrapper, RDFXML
from SPARQLWrapper.Wrapper import QueryResult

def handler(request):
        
    query_as_url_encoded_str = request.args.get("query", None)
    if not query_as_url_encoded_str:
        logging.error('Aborting, no query string recieved')
        return 'No query string received', 404

    query = parse.unquote(query_as_url_encoded_str)

    sparql = SPARQLWrapper("http://staging.gss-data.org.uk/sparql")
    sparql.setQuery(query)

    sparql.setReturnFormat(RDFXML)
    results: QueryResult = sparql.query().convert()

    context = {"@vocab": "http://purl.org/dc/terms/", "@language": "en"}
    resp = Response(results.serialize(format='json-ld', context=context, indent=4))

    headers = {'Content-Type': 'application/ld+json'}
    return resp, 200, headers