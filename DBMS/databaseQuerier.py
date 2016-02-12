#!/usr/bin/python3

import os
import rdflib

DATABASE = os.path.abspath(os.path.join(os.path.dirname(__file__), "../database"))

class DatabaseQuerier:

    def __init__(self, databaseDirectory=DATABASE):
        self.graph = rdflib.Graph()

        for fileName in os.listdir(databaseDirectory):
            filePath = os.path.abspath(os.path.join(DATABASE, fileName))
            self.graph.parse(filePath, format="turtle")

    # TODO: fix syntax error with query
    def query(self, surname=None, forename=None, title=None, occupation=None, address=None, year=None):
        prefixes = "PREFIX ns1: <http://schema.org/Person#> .\n" \
                   "PREFIX ns2: <http://purl.org/dc/terms/> .\n" \
                   "PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .\n" \
                   "PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#> .\n" \
                   "PREFIX xml: <http://www.w3.org/XML/1998/namespace> .\n" \
                   "PREFIX xsd: <http://www.w3.org/2001/XMLSchema#> .\n"

        selectStatement = "SELECT ?surname ?forename ?title ?occupation ?address ?year\n"
        whereStatement = "WHERE {\n" \
                         "  ?d ns1:familyName ?surname .\n" \
                         "  OPTIONAL { ?d ns1:givenName ?forename . }\n" \
                         "  OPTIONAL { ?d ns1:honorificPrefix ?title . }\n" \
                         "  OPTIONAL { ?d ns1:jobTitle ?occupation . }\n" \
                         "  OPTIONAL { ?d ns1:address ?address . }\n" \
                         "  ?d ns2:issued ?year\n"

        if surname:
            whereStatement += "  ?d ns1:familyName {0} .\n".format(surname)

        if forename:
            whereStatement += " ?d ns1:givenName {0} .\n".format(forename)

        if title:
            whereStatement += " ?d ns1:honorificPrefix {0} .\n".format(title)

        if occupation:
            whereStatement += " ?d ns1:jobTitle {0} .\n".format(occupation)

        if address:
            whereStatement += " ?d ns1:address {0} .\n".format(address)

        if year:
            whereStatement += " ?d ns2:issued {0} .\n".format(year)

        whereStatement += "}"

        query = prefixes + selectStatement + whereStatement

        print(query)

        return self.graph.query(query)

if __name__ == "__main__":
    d = DatabaseQuerier()
    print(d.query(surname="Abernethy"))
