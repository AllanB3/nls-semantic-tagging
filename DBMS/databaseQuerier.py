#!/usr/bin/python3

import os
import rdflib

DATABASE = os.path.abspath(os.path.join(os.path.dirname(__file__), "../database/data.ttl"))

class DatabaseQuerier:

    def __init__(self, database=DATABASE):
        self.graph = rdflib.Graph()
        self.graph.parse(database, format="turtle")

    def query(self, surname=None, forename=None, title=None, occupation=None, address=None, latitude=None,
              longitude=None, year=None):
        prefixes = "PREFIX ns1: <http://schema.org/Person#>\n" \
                   "PREFIX ns2: <http://schema.org/GeoCoordinates#>\n" \
                   "PREFIX ns3: <http://purl.org/dc/terms/>\n" \
                   "PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>\n" \
                   "PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>\n" \
                   "PREFIX xml: <http://www.w3.org/XML/1998/namespace>\n" \
                   "PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>\n"

        selectStatement = "SELECT ?surname ?forename ?title ?occupation ?address ?lat ?lon ?year\n"
        whereStatement = "WHERE {\n" \
                         "  ?d ns1:familyName ?surname .\n" \
                         "  OPTIONAL { ?d ns1:givenName ?forename . }\n" \
                         "  OPTIONAL { ?d ns1:honorificPrefix ?title . }\n" \
                         "  OPTIONAL { ?d ns1:jobTitle ?occupation . }\n" \
                         "  OPTIONAL { ?d ns1:address ?address . }\n" \
                         "  OPTIONAL { ?d ns2:latitude ?lat . }\n"\
                         "  OPTIONAL { ?d ns2:longitude ?lon . }\n"\
                         "  ?d ns3:issued ?year .\n"

        if surname is not None:
            whereStatement += "  ?d ns1:familyName \"{0}\" .\n".format(surname)

        if forename is not None:
            whereStatement += " ?d ns1:givenName \"{0}\" .\n".format(forename)

        if title is not None:
            whereStatement += " ?d ns1:honorificPrefix \"{0}\" .\n".format(title)

        if occupation is not None:
            whereStatement += " ?d ns1:jobTitle \"{0}\" .\n".format(occupation)

        if address is not None:
            whereStatement += " ?d ns1:address \"{0}\" .\n".format(address)

        if latitude is not None:
            whereStatement += " ?d ns2:latitude \"{0}\" .\n".format(latitude)

        if longitude is not None:
            whereStatement += " ?d ns2:longitude \"{0}\" .\n".format(longitude)

        if year is not None:
            whereStatement += " ?d ns3:issued \"{0}\" .\n".format(year)

        whereStatement += "}"

        query = prefixes + selectStatement + whereStatement

        queryResult = self.graph.query(query)
        formattedResult = []
        fields = ["surname", "forename", "title", "occupation", "address", "latitude", "longitude", "year"]

        for record in queryResult:
            formattedRecord = {}
            for i, field in enumerate(record):
                if field is not None:
                    formattedRecord[fields[i]] = field.value
                else:
                    formattedRecord[fields[i]] = None

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

    print("COORDS:")
    results = d.query(latitude="55.9128487", longitude="-3.1615066")
    for r in results:
        print(r)
    print("")

    print("YEAR:")
    results = d.query(year="1851")
    for r in results:
        print(r)
