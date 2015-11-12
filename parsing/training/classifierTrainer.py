#!/usr/bin/python

import sys
import os

trainingFolder = os.abspath(os.path.join(os.path.dirname(__file__), sys.argv[0]))
trainingOutputPath = os.abspath(os.path.join(os.path.dirname(__file__), sys.argv[1]))
trainingOutputFile = open(trainingOutputPath, "w")

for fileName in os.listdir(trainingFolder):
    tags = []
    trainingValues = open(trainingFolder, "r").read()

    for c in trainingValues:
        if c == "(":
            trainingValue = ""