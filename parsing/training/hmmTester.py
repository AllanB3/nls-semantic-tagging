#!/usr/bin/python3

from __future__ import division
import sys
import os

TESTINGFOLDER = os.path.join(os.path.abspath(os.path.dirname(__file__)), "hmmDevTest")

from tabulate import tabulate

sys.path.insert(1, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from hiddenMarkovModel import *
from xmlParser import *

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

hmm = hiddenMarkovModel()
x = XMLParser()

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

    text = x._parseNLSPage(xmlFile)
    classifiedTags = hmm.tag(text)

    annFileText = open(annFile, "r").read().splitlines()

    classifiedCounter = 0
    for a in annFileText:
        if a[0] == "E":
            continue

        _, tokenData, actualToken = a.strip().split("\t")
        actualTag = tokenData.split()[0].upper()
        startIndex = tokenData.split()[1]

        if actualTag == "POD_ENTRY":
            continue

        for word in actualToken.split(","):
            classifiedToken, classifiedTag = classifiedTags[classifiedCounter]

            if classifiedToken.replace(" ", "") != word.replace(" ", ""):
                if ((classifiedTags[classifiedCounter][0] + classifiedTags[classifiedCounter + 1][0]).replace(" ", "") ==
                    actualToken.replace(" ", "")):
                    classifiedToken = classifiedTags[classifiedCounter][0] + " " + classifiedTags[classifiedCounter + 1][0]
                    classifiedCounter += 1
                else:
                    raise ValueError("HMM output and BRAT output misaligned. Expected {0} and got {1}.".format(word,
                                                                                                            classifiedToken))

            confusionMatrix[actualTag][classifiedTag] += 1

            if actualTag == classifiedTag:
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

            print("Token: " + word)
            print("Actual tag: " + actualTag)
            print("Classified tag: " + classifiedTag)
            print("")
            classifiedCounter += 1

scores = {"SURNAME": {"Precision": 0, "Recall": 0, "F-score": 0},
          "FORENAME": {"Precision": 0, "Recall": 0, "F-score": 0},
          "TITLE": {"Precision": 0, "Recall": 0, "F-score": 0},
          "OCCUPATION": {"Precision": 0, "Recall": 0, "F-score": 0},
          "ADDRESS": {"Precision": 0, "Recall": 0, "F-score": 0}}

for tag, tagResults in results.items():
    try:
        precision = tagResults["TP"] / (tagResults["TP"] + tagResults["FP"])
    except ZeroDivisionError:
        precision = "N/A"
    scores[tag]["Precision"] = precision

    try:
        recall = tagResults["TP"] / (tagResults["TP"] + tagResults["FN"])
    except ZeroDivisionError:
        recall = "N/A"
    scores[tag]["Recall"] = recall

    if recall != "N/A" and precision != "N/A":
        try:
            scores[tag]["F-score"] = (2 * precision * recall) / (precision + recall)
        except ZeroDivisionError:
            scores[tag]["F-score"] = "N/A"
    else:
        scores[tag]["F-score"] = "N/A"

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