#!/usr/bin/python3

import pathlib
import os
import rdflib
from databaseQuerier import *
import sys
import editdistance

DATABASE = os.path.abspath(os.path.join(os.path.dirname(__file__), "../database"))

class RecordLinker:

    def __init__(self, database=DATABASE):
        self.databaseURI = pathlib.PurePath(database).joinpath("data.ttl").as_uri()
        self.graph = rdflib.Graph()
        self.graph.parse(self.databaseURI, format="turtle")
        self.querier = DatabaseQuerier(os.path.abspath(os.path.join(database, "data.ttl")))

    def findMatches(self, record):
        bkv = record["bkv"]

        results = self.querier.query(bkv=bkv)
        matchingRecords = [record]

        for r in results:
            if int(editdistance.eval(r["surname"], record["surname"])) < 2 \
               and int(editdistance.eval(r["forename"], record["forename"])) < 2 \
               and int(editdistance.eval(r["title"], record["title"])) < 2 \
               and int(editdistance.eval(r["occupation"], record["occupation"])) < 2 \
               and int(editdistance.eval(r["address"], record["address"])) < 2:
                matchingRecords.append(r)

        return matchingRecords

    def findAllMatches(self):
        schema = rdflib.Namespace("http://schema.org/")
        records = self.querier.query()

        for r in records:
            matches = self.findMatches(r)

            for m in matches:
                self.graph.add((r["uri"], schema.sameAs, m["uri"]))

        self.graph.serialize(self.databaseURI, format="turtle")

if __name__ == "__main__":
    try:
        linker = RecordLinker(sys.argv[1])
    except IndexError:
        linker = RecordLinker()

    linker.findAllMatches()
