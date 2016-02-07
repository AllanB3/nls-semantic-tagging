#!/usr/bin/python3

from __future__ import division
import sys
import os

TESTINGFOLDER = os.path.join(os.path.abspath(os.path.dirname(__file__)), "hmmDevTest")
sys.path.insert(1, os.path.join(os.path.abspath(os.path.dirname(__file__)), ".."))
from entryExtractor import *

results = {"TP": 0, "TN": 0, "FP": 0, "FN": 0}

entryExtractor = EntryExtractor()

totalRecords = 0
for dirName in os.listdir(TESTINGFOLDER):
    dirPath = os.path.abspath(os.path.join(TESTINGFOLDER, dirName))
    xmlFile = ""
    annFile = ""

    for testFile in os.listdir(dirPath):
        fileExtension = testFile[-3:]

        if fileExtension == "xml":
            xmlFile = os.path.join(os.path.join(TESTINGFOLDER, dirName), testFile)
        elif fileExtension == "ann":
            annFile = os.path.join(os.path.join(TESTINGFOLDER, dirName), testFile)

    if xmlFile == "" or annFile == "":
        raise IOError("Test folder must have an XML file of the page from the NLS and a corresponding brat ann file.")

    retrievedRecords = entryExtractor.extractFeatures(xmlFile, "page")

    annFileText = open(annFile, "r").read().splitlines()
    tokens = {}
    records = []
    for a in annFileText:
        if a[0] == "E":
            continue

        key, _, token = a.strip().split("\t")
        tokens[key] = token

    for a in annFileText:
        if a[0] == "T":
            continue

        record = {}
        _, value = a.strip().split("\t", 1)

        for v in value.split():
            tag, tokenKey = v.split(":")

            if tag == "address2":
                record["ADDRESS"] = record["ADDRESS"] + ", {0}".format(tokens[tokenKey])
            elif tag == "POD_entry":
                record["SURNAME"] = tokens[tokenKey]
            else:
                record[tag.upper()] = tokens[tokenKey]

        records.append(record)

    for r in retrievedRecords:
        if r in records:
            results["TP"] += 1
        else:
            results["FP"] += 1
    totalRecords += len(records)

results["FN"] = totalRecords - results["TP"]

precision = results["TP"] / (results["TP"] + results["FP"])
recall = results["TP"] / (results["TP"] + results["FN"])
fScore = (2 * precision * recall) / (precision + recall)

print("Precision: {0}".format(precision))
print("Recall: {0}".format(recall))
print("F-score: {0}".format(fScore))
