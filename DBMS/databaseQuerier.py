#!/usr/bin/python3

import os
import rdflib
import optparse

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

        selectStatement = "SELECT ?d ?surname ?forename ?title ?occupation ?address ?lat ?lon ?year ?bkv\n"
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
        fields = ["uri", "surname", "forename", "title", "occupation", "address", "latitude", "longitude", "year",
                  "bkv"]

        for record in queryResult:
            formattedRecord = {}
            for i, field in enumerate(record):
                if field is not None:
                    try:
                        formattedRecord[fields[i]] = field.value
                    except AttributeError:
                        formattedRecord[fields[i]] = str(field)
                else:
                    formattedRecord[fields[i]] = "None"

            formattedResult.append(formattedRecord)

        return formattedResult

if __name__ == "__main__":
    querier = DatabaseQuerier()

    optparser = optparse.OptionParser()
    optparser.add_option("-s", "--surname", dest="surname", default=None, help="Surname to search database by.")
    optparser.add_option("-f", "--forename", dest="forename", default=None, help="Forename to search database by.")
    optparser.add_option("-t", "--title", dest="title", default=None, help="Title to search database by.")
    optparser.add_option("-j", "--job", dest="occupation", default=None, help="Occupation to search database by.")
    optparser.add_option("-a", "--address", dest="address", default=None, help="Address to search database by.")
    optparser.add_option("-l", "--lat", dest="latitude", default=None, help="Latitude to search database by.")
    optparser.add_option("-o", "--lon", dest="longitude", default=None, help="Longitude to search database by.")
    optparser.add_option("-y", "--year", dest="year", default=None, help="Year to search database by.")
    optparser.add_option("-b", "--bkv", dest="bkv", default=None, help="Block key value to search database by.")
    (opts, _) = optparser.parse_args()

    results = querier.query(surname=opts.surname, forename=opts.forename, title=opts.title, occupation=opts.occupation,
                            address=opts.address, latitude=opts.latitude, longitude=opts.longitude, year=opts.year,
                            bkv=opts.bkv)

    for r in results:
        print(r)
