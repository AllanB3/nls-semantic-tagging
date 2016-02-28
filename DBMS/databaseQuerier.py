#!/usr/bin/python3

import os
import rdflib

DATABASE = os.path.abspath(os.path.join(os.path.dirname(__file__), "../database/data.ttl"))

class DatabaseQuerier:

    def __init__(self, database=DATABASE):
        self.graph = rdflib.Graph()
        self.graph.parse(database, format="turtle")

    def query(self, surname=None, forename=None, title=None, occupation=None, address=None, latitude=None,
              longitude=None, year=None, bkv=None):
        prefixes = "PREFIX person: <http://schema.org/Person#>\n" \
                   "PREFIX geo: <http://schema.org/GeoCoordinates#>\n" \
                   "PREFIX dcat: <http://purl.org/dc/terms/>\n" \
                   "PREFIX pod: <file:///home/allan/Documents/University/Fourth-Year/PROJ/nls-semantic-tagging/" \
                   "database/postOfficeRecord.ttl%23>\n" \
                   "PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>\n" \
                   "PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>\n" \
                   "PREFIX xml: <http://www.w3.org/XML/1998/namespace>\n" \
                   "PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>\n"

        selectStatement = "SELECT ?surname ?forename ?title ?occupation ?address ?lat ?lon ?year ?bkv\n"
        whereStatement = "WHERE {\n" \
                         "  ?d person:familyName ?surname .\n" \
                         "  OPTIONAL { ?d person:givenName ?forename . }\n" \
                         "  OPTIONAL { ?d person:honorificPrefix ?title . }\n" \
                         "  OPTIONAL { ?d person:jobTitle ?occupation . }\n" \
                         "  OPTIONAL { ?d person:address ?address . }\n" \
                         "  OPTIONAL { ?d geo:latitude ?lat . }\n" \
                         "  OPTIONAL { ?d geo:longitude ?lon . }\n" \
                         "  ?d dcat:issued ?year .\n" \
                         "  ?d pod:blockKeyValue ?bkv .\n"

        if surname is not None:
            whereStatement += "  ?d person:familyName \"{0}\" .\n".format(surname)

        if forename is not None:
            whereStatement += " ?d person:givenName \"{0}\" .\n".format(forename)

        if title is not None:
            whereStatement += " ?d person:honorificPrefix \"{0}\" .\n".format(title)

        if occupation is not None:
            whereStatement += " ?d person:jobTitle \"{0}\" .\n".format(occupation)

        if address is not None:
            whereStatement += " ?d person:address \"{0}\" .\n".format(address)

        if latitude is not None:
            whereStatement += " ?d geo:latitude \"{0}\" .\n".format(latitude)

        if longitude is not None:
            whereStatement += " ?d geo:longitude \"{0}\" .\n".format(longitude)

        if year is not None:
            whereStatement += " ?d dcat:issued \"{0}\" .\n".format(year)

        if bkv is not None:
            whereStatement += " ?d pod:blockKeyValue \"{0}\" .\n".format(bkv)

        whereStatement += "}"

        query = prefixes + selectStatement + whereStatement

        queryResult = self.graph.query(query)
        formattedResult = []
        fields = ["surname", "forename", "title", "occupation", "address", "latitude", "longitude", "year", "bkv"]

        for record in queryResult:
            formattedRecord = {}
            for i, field in enumerate(record):
                if field is not None:
                    formattedRecord[fields[i]] = field.value
                else:
                    formattedRecord[fields[i]] = "None"

            formattedResult.append(formattedRecord)

        return formattedResult

if __name__ == "__main__":
    d = DatabaseQuerier()

    print("SURNAME:")
    results = d.query(surname="Abernethy")
    for r in results:
        print(r)
    print("")

    print("FORENAME:")
    results = d.query(forename="Scott")
    for r in results:
        print(r)
    print("")

    print("TITLE:")
    results = d.query(title="Miss")
    for r in results:
        print(r)
    print("")

    print("OCCUPATION:")
    results = d.query(occupation="watchmaker")
    for r in results:
        print(r)
    print("")

    print("ADDRESS:")
    results = d.query(address="90 Kirkgate")
    for r in results:
        print(r)
    print("")

    print("YEAR:")
    results = d.query(latitude="55.9128487", longitude="-3.1615066")
    for r in results:
        print(r)

    results = d.query(year="1851")
    for r in results:
        print(r)
    print("")

    print("BKV:")
    results = d.query(bkv="ABE90KIR")
    for r in results:
        print(r)
