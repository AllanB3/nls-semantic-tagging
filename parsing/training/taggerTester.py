#!/usr/bin/python

import sys
import os
from tabulate import tabulate
from arffParser import *

sys.path.insert(1, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from tokenClassifier import *

results = {
    "SURNAME": {"TP": 0, "FP": 0, "TN": 0, "FN": 0},
    "FORENAME": {"TP": 0, "FP": 0, "TN": 0, "FN": 0},
    "TITLE": {"TP": 0, "FP": 0, "TN": 0, "FN": 0},
    "OCCUPATION": {"TP": 0, "FP": 0, "TN": 0, "FN": 0},
    "ADDRESS": {"TP": 0, "FP": 0, "TN": 0, "FN": 0}
}

confusionMatrix = {
    "SURNAME": {"SURNAME": 0, "FORENAME": 0, "TITLE": 0, "OCCUPATION": 0, "ADDRESS": 0},
    "FORENAME": {"SURNAME": 0, "FORENAME": 0, "TITLE": 0, "OCCUPATION": 0, "ADDRESS": 0},
    "TITLE": {"SURNAME": 0, "FORENAME": 0, "TITLE": 0, "OCCUPATION": 0, "ADDRESS": 0},
    "OCCUPATION": {"SURNAME": 0, "FORENAME": 0, "TITLE": 0, "OCCUPATION": 0, "ADDRESS": 0},
    "ADDRESS": {"SURNAME": 0, "FORENAME": 0, "TITLE": 0, "OCCUPATION": 0, "ADDRESS": 0}
}

os.chdir(os.path.abspath(os.path.join(os.path.dirname(__file__), "../training")))
tagger = tokenClassifier("training.arff")
tagger.train()

os.chdir(os.path.abspath(os.path.dirname(__file__)))

dataset = arffParser.parseFile("testing.arff")
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

    confusionMatrix[actualTag][classifiedTag] += 1

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

confusion = [["", "SURNAME", "FORENAME", "TITLE", "OCCUPATION", "ADDRESS"],
             ["SURNAME", confusionMatrix["SURNAME"]["SURNAME"], confusionMatrix["SURNAME"]["FORENAME"],
              confusionMatrix["SURNAME"]["TITLE"], confusionMatrix["SURNAME"]["OCCUPATION"],
              confusionMatrix["SURNAME"]["ADDRESS"]],
             ["FORENAME", confusionMatrix["FORENAME"]["SURNAME"], confusionMatrix["FORENAME"]["FORENAME"],
              confusionMatrix["FORENAME"]["TITLE"], confusionMatrix["FORENAME"]["OCCUPATION"],
              confusionMatrix["FORENAME"]["ADDRESS"]],
             ["TITLE", confusionMatrix["TITLE"]["SURNAME"], confusionMatrix["TITLE"]["FORENAME"],
              confusionMatrix["TITLE"]["TITLE"], confusionMatrix["TITLE"]["OCCUPATION"],
              confusionMatrix["TITLE"]["ADDRESS"]],
             ["OCCUPATION", confusionMatrix["OCCUPATION"]["SURNAME"], confusionMatrix["OCCUPATION"]["FORENAME"],
              confusionMatrix["OCCUPATION"]["TITLE"], confusionMatrix["OCCUPATION"]["OCCUPATION"],
              confusionMatrix["OCCUPATION"]["ADDRESS"]],
             ["ADDRESS", confusionMatrix["ADDRESS"]["SURNAME"], confusionMatrix["ADDRESS"]["FORENAME"],
              confusionMatrix["ADDRESS"]["TITLE"], confusionMatrix["ADDRESS"]["OCCUPATION"],
              confusionMatrix["ADDRESS"]["ADDRESS"]]]

print(tabulate(table))
print("")
print(tabulate(confusion))