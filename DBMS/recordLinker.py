#!/usr/bin/python3

import pathlib
import os
import rdflib
from databaseQuerier import *
from tabulate import tabulate
import sys
import editdistance

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
            if int(editdistance.eval(r["surname"], record["surname"])) < 2 \
               and int(editdistance.eval(r["forename"], record["forename"])) < 2 \
               and int(editdistance.eval(r["title"], record["title"])) < 2 \
               and int(editdistance.eval(r["occupation"], record["occupation"])) < 2 \
               and int(editdistance.eval(r["address"], record["address"])) < 2:
                matchingRecords.append(r)

        return matchingRecords

    def findAllMatches(self):
        records = self.querier.query()
        matches = {}

        for r in records:
            rString = str(r)
            if rString in matches:
                continue

            print("SURNAME: {0}".format(r["surname"].encode("utf-8")))
            print("FORENAME: {0}".format(r["forename"].encode("utf-8")))
            print("TITLE: {0}".format(r["title"].encode("utf-8")))
            print("OCCUPATION: {0}".format(r["occupation"].encode("utf-8")))
            print("ADDRESS: {0}".format(r["address"].encode("utf-8")))

            matches[rString] = self.findMatches(r)
            sys.stdout.write("YEARS: {0}".format(r["year"]))

            for m in matches[rString]:
                sys.stdout.write(", {0}".format(m["year"]))
            print("\n")

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
