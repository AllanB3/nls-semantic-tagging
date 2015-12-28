#!/usr/bin/python

import sys
import os

TESTINGFOLDER = os.path.join(os.path.abspath(os.path.dirname(__file__)), "hmmTestingData")

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
x = xmlParser()

for dirName in os.listdir(TESTINGFOLDER):
    dirPath = os.path.abspath(os.path.join(TESTINGFOLDER, dirName))
    xmlFile = ""
    annFile = ""

    for testFile in os.listdir(dirPath):
        fileExtension = testFile[-3:]

        if fileExtension == "xml":
            xmlFile = os.path.join(TESTINGFOLDER, testFile)
        elif fileExtension == "ann":
            annFile = os.path.join(TESTINGFOLDER, testFile)

    if xmlFile == "" or annFile == "":
        raise IOError("Test folder must have an XML file of the page from the NLS and a corresponding brat ann file.")

    text = x.parseNLSPage(xmlFile)
    tags = hmm.tag(text)

    # TODO: figure out a way to align tags from the HMM and tags from brat.