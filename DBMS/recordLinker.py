#!/usr/bin/python3

import pathlib
import os
import rdflib
from databaseQuerier import *
from tabulate import tabulate

DATABASE = os.path.abspath(os.path.join(os.path.dirname(__file__), "../database"))

class RecordLinker:

    def __init__(self, database=DATABASE):
        databaseURI = pathlib.PurePath(database).joinpath("data.ttl").as_uri()
        self.graph = rdflib.Graph()
        self.graph.parse(databaseURI, format="turtle")
        self.querier = DatabaseQuerier(os.path.abspath(os.path.join(database, "data.ttl")))

    def findMatches(self, record):
        bkv = record["bkv"]

        results = self.querier.query(bkv=bkv)
        matchingRecords = [record]

        for r in results:
            if r == record:
                continue

            if r["surname"] == record["surname"] and r["forename"] == record["forename"] \
               and r["title"] == record["title"] and r["occupation"] == record["occupation"] \
               and r["address"] == record["address"]:
                matchingRecords.append(r)

        return matchingRecords

    def findAllMatches(self):
        records = self.querier.query()
        matches = {}

        for r in records:
            rString = str(r)
            if rString in matches:
                continue

            matches[rString] = self.findMatches(r)

        return matches

if __name__ == "__main__":
    table = [["SURNAME", "FORENAME", "TITLE", "OCCUPATION", "ADDRESS", "YEARS"]]

    recordLinker = RecordLinker()
    results = recordLinker.findAllMatches()

    for key, value in results.items():
        result = eval(key)
        resultData = [result["surname"], result["forename"], result["title"], result["occupation"], result["address"],
                      result["year"]]

        for v in value:
            resultData[-1] += ", {0}".format(v["year"])

        table.append(resultData)

    print(tabulate(table))