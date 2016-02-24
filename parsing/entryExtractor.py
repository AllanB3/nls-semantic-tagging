#!/usr/bin/python3

from hiddenMarkovModel import *
from xmlParser import *
import rdflib
from rdflib.namespace import RDF, OWL, RDFS
import pathlib
import os
import hashlib
import urllib.request
import xml.etree.ElementTree as ET
from collections import defaultdict
import pyparsing

import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../DBMS")))
from databaseQuerier import *

DATABASE = pathlib.PurePath(os.path.abspath(os.path.join(os.path.dirname(__file__), "../database")))

class EntryExtractor:

    def __init__(self):
        self.xmlParser = xmlParser()
        self.hiddenMarkovModel = hiddenMarkovModel()

    def extractFeatures(self, filePath, source):
        if source == "ocr":
            text = self.xmlParser.parseOCR(filePath)
        elif source == "page":
            text = self.xmlParser.parseNLSPage(filePath)
        elif source == "directory":
            text = self.xmlParser.parseNLSDirectory(filePath)
        else:
            raise IOError("source must equal \"ocr\", \"directory\" or \"page\"")

        tokensAndTags = self.hiddenMarkovModel.tag(text)

        entries = []
        nextTags = {"SURNAME": ["FORENAME", "TITLE"], "FORENAME": ["OCCUPATION", "ADDRESS"], "TITLE": ["FORENAME", "OCCUPATION", "ADDRESS"], "OCCUPATION": ["OCCUPATION", "ADDRESS"], "ADDRESS": ["ADDRESS"]}
        entry = defaultdict(lambda: None)
        previousTag = "SURNAME"
        for token, tag in tokensAndTags:
            if not tag in nextTags[previousTag]:
                entries.append(entry)
                entry = defaultdict(lambda: None)

                if not tag == "SURNAME":
                    continue

            if not tag in entry:
                entry[tag] = token.lstrip().strip()
            else:
                entry[tag] = entry[tag] + ", "  + token.lstrip().strip()

            previousTag = tag

        return entries

    @staticmethod
    def addRecordsToDatabase(records, recordYear):
        g = rdflib.Graph()
        schema = rdflib.Namespace("http://schema.org/")
        person = rdflib.Namespace("http://schema.org/Person#")
        dcat = rdflib.Namespace("https://www.w3.org/ns/dcat#")
        dct = rdflib.Namespace("http://purl.org/dc/terms/")
        geoCoordinates = rdflib.Namespace("http://schema.org/GeoCoordinates#")
        postOfficeRecordSchema = rdflib.Namespace(DATABASE.joinpath("postOfficeRecord.owl#").as_uri())

        uri = DATABASE.joinpath("data.ttl").as_uri()

        databaseExists = False
        try:
            g.parse(DATABASE.joinpath("data.ttl").__str__(), format="turtle")
            databaseExists = True
            databaseQuerier = DatabaseQuerier()
        except FileNotFoundError:
            schemaGraph = rdflib.Graph()

            schemaURI = DATABASE.joinpath("postOfficeRecord.owl").as_uri()
            schemaGraph.add((rdflib.URIRef(schemaURI), RDF.type, OWL.ontology))

            postOfficeRecord = rdflib.URIRef(schemaURI + "#PostOfficeRecord")
            schemaGraph.add((postOfficeRecord, RDF.type, OWL.Class))
            schemaGraph.add((postOfficeRecord, RDFS.subClassOf, dcat.CatalogRecord))

            blockKeyValue = rdflib.URIRef(schemaURI + "#blockKeyValue")
            schemaGraph.add((blockKeyValue, RDF.type, RDF.Property))
            schemaGraph.add((blockKeyValue, RDFS.comment, rdflib.Literal("A block key value for comparing the record to"
                                                                    " similar records during data deduplication/record"
                                                                    " linkage.")))
            schemaGraph.add((blockKeyValue, RDFS.label, rdflib.Literal("Block key value")))

            schemaGraph.serialize(schemaURI, format="turtle")

        for r in records:
            if not ("SURNAME" in r and "ADDRESS" in r):
                continue

            if databaseExists:
                try:
                    existingRecords = databaseQuerier.query(surname=r["SURNAME"], forename=r["FORENAME"], title=r["TITLE"],
                                                            occupation=r["OCCUPATION"], address=r["ADDRESS"], year=recordYear)
                except pyparsing.ParseException:
                    continue

                if len(existingRecords) > 0:
                    continue

            recordData = "".join(value for key, value in r.items() if value is not None) + str(recordYear)
            identifier = rdflib.URIRef("{0}#{1}".format(uri, hashlib.md5(recordData.encode("utf-8")).hexdigest()))

            g.add((identifier, person.additionalType, postOfficeRecordSchema.PostOfficeRecord))
            g.add((identifier, dct.issued, rdflib.Literal(recordYear)))
            g.add((identifier, RDF.type, schema.Person))

            bkv = "".join(l for l in r["SURNAME"].upper() if l.isalpha())[:3]
            for word in r["ADDRESS"].split():
                bkv += "".join(l for l in word.upper() if l.isalpha() or l.isdigit())[:3]

            g.add((identifier, postOfficeRecordSchema.blockKeyValue, rdflib.Literal(bkv)))

            for key, value in r.items():
                if key == "SURNAME":
                    relation = person.familyName
                elif key == "FORENAME":
                    relation = person.givenName
                elif key == "TITLE":
                    relation = person.honorificPrefix
                elif key == "OCCUPATION":
                    relation = person.jobTitle
                elif key == "ADDRESS":
                    relation = person.address
                else:
                    raise ValueError("{0} is not a valid key".format(key))

                g.add((identifier, relation, rdflib.Literal(value)))

            openStreetMapData = urllib.request.urlopen("http://nominatim.openstreetmap.org/search?format=xml&polygon=1"
                                                       "&q={0}".format(r["ADDRESS"].replace(" ", "+").encode("utf-8")) +
                                                       ",+edinburgh")
            responseTree = ET.fromstring(openStreetMapData.read())

            try:
                addressData = responseTree[0]
                latitude = ""
                longitude = ""

                for key, value in addressData.attrib.items():
                    if key == "lat" and value != "":
                        latitude = value
                    elif key == "lon" and value != "":
                        longitude = value

                g.add((identifier, geoCoordinates.latitude, rdflib.Literal(latitude)))
                g.add((identifier, geoCoordinates.longitude, rdflib.Literal(longitude)))
            except IndexError:
                pass

        g.serialize(uri, format="turtle")

if __name__ == "__main__":
    e = EntryExtractor()

    entries = e.extractFeatures("training/hmmDevTest/1911-12-p96/84311938.8.xml", "page")
    e.addRecordsToDatabase(entries, "1911")

    entries = e.extractFeatures("training/hmmDevTest/1851-52-p43/83072360.8.xml", "page")
    e.addRecordsToDatabase(entries, "1851")

    entries = e.extractFeatures("training/hmmDevTest/1940-41-p110/1940-41-p110.xml", "page")
    e.addRecordsToDatabase(entries, "1940")

    entries = e.extractFeatures("training/hmmDevTest/1940-41-p365/1940-41-p365.xml", "page")
    e.addRecordsToDatabase(entries, "1940")
