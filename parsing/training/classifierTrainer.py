#!/usr/bin/python

import sys
import os
import arff

trainingFolder = os.path.abspath(os.path.join(os.path.dirname(__file__), sys.argv[1]))
trainingOutputPath = os.path.abspath(os.path.join(os.path.dirname(__file__), sys.argv[2]))
trainingOutputFile = open(trainingOutputPath, "w")

for fileName in os.listdir(trainingFolder):
    tagsAndVectors = []

    # TODO: replace this with xmlparser
    trainingValues = open(os.path.abspath(os.path.join(trainingFolder, fileName)), "r").read()

    currentValue = ""
    currentTag = ""
    addingValue = False
    addingTag = False

    previousValue = ""
    tokenLength = 0
    digits = 0
    dictionaryTags = []

    featureVector = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, ""]

    for c in trainingValues:
        if c == "(":
            addingValue = True

            if not len(tagsAndVectors) == 0:
                previousValue = tagsAndVectors[len(tagsAndVectors) - 1][10]

        if addingValue:
            if not c == "[":
                currentValue += c

                tokenLength += 1
                if c.isdigit():
                    digits += 1
            else:
                addingValue = False
                addingTag = True

                #TODO: lexicon lookup here and build feature vector

                currentValue = ""
                continue

        if addingTag:
            if not c == "]":
                currentTag += c
            else:
                tagsAndVectors.append(featureVector)
                currentTag = ""
                addingTag = False


arff.dump(trainingOutputPath, tagsAndVectors, relation="Post Office Data")