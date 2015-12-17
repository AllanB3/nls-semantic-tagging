#!/usr/bin/python

import sys
import os
import numpy
from tabulate import tabulate

sys.path.insert(1, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from tokenClassifier import *

results = {
    "SURNAME": {"TP": 0, "FP": 0, "TN": 0, "FN": 0},
    "FORENAME": {"TP": 0, "FP": 0, "TN": 0, "FN": 0},
    "TITLE": {"TP": 0, "FP": 0, "TN": 0, "FN": 0},
    "OCCUPATION": {"TP": 0, "FP": 0, "TN": 0, "FN": 0},
    "ADDRESS": {"TP": 0, "FP": 0, "TN": 0, "FN": 0}
}

os.chdir(os.path.abspath(os.path.join(os.path.dirname(__file__), "../training")))
tagger = tokenClassifier("training.arff")
tagger.train()

os.chdir(os.path.abspath(os.path.dirname(__file__)))

testingData = open("testing.arff", "r").read().splitlines()
dataStart = testingData.index("@data")

data = []

for t in testingData[dataStart + 1:]:
    data.append(t.split(","))

dataset = numpy.asanyarray(data)
testingValues = dataset[:,:12]
testingClasses = dataset[:,12]

i = 0
for t in testingClasses:
    testingClasses[i] = t.replace("\'", "")
    i += 1

i = 0
while i < len(testingValues):
    classifiedTag = tagger.classify(testingValues[i])
    actualTag = testingClasses[i]

    if classifiedTag == actualTag:
        results[actualTag]["TP"] += 1

        for tag, tagResults in results.items():
            if tag != actualTag:
                tagResults["TN"] += 1
    else:
        results[actualTag]["FN"] += 1
        results[classifiedTag]["FP"] += 1

        for tag, tagResults in results.items():
            if tag != actualTag and tag != classifiedTag:
                tagResults["TN"] += 1

    i += 1

scores = {"SURNAME": {"Precision": 0, "Recall": 0, "F-score": 0},
          "FORENAME": {"Precision": 0, "Recall": 0, "F-score": 0},
          "TITLE": {"Precision": 0, "Recall": 0, "F-score": 0},
          "OCCUPATION": {"Precision": 0, "Recall": 0, "F-score": 0},
          "ADDRESS": {"Precision": 0, "Recall": 0, "F-score": 0}}

for tag, tagResults in results.items():
    precision = tagResults["TP"] / (tagResults["TP"] + tagResults["FP"])
    scores[tag]["Precision"] = precision

    recall = tagResults["TP"] / (tagResults["TP"] + tagResults["FN"])
    scores[tag]["Recall"] = recall

    scores[tag]["F-score"] = (2 * precision * recall) / (precision + recall)

table = [["", "SURNAME", "FORENAME", "TITLE", "OCCUPATION", "ADDRESS"],
         ["Precision", scores["SURNAME"]["Precision"], scores["FORENAME"]["Precision"],
          scores["TITLE"]["Precision"], scores["OCCUPATION"]["Precision"],
          scores["ADDRESS"]["Precision"]],
         ["Recall", scores["SURNAME"]["Recall"], scores["FORENAME"]["Recall"],
          scores["TITLE"]["Recall"], scores["OCCUPATION"]["Recall"],
          scores["ADDRESS"]["Recall"]],
         ["F-score", scores["SURNAME"]["F-score"], scores["FORENAME"]["F-score"],
          scores["TITLE"]["F-score"], scores["OCCUPATION"]["F-score"],
          scores["ADDRESS"]["F-score"]]]

print(tabulate(table))