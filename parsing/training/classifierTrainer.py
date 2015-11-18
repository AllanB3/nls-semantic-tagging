#!/usr/bin/python

import sys
import os
import arff

path = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(1, path)

from xmlparser import *

trainingFolder = os.path.abspath(os.path.join(os.path.dirname(__file__), sys.argv[1]))
trainingOutputPath = os.path.abspath(os.path.join(os.path.dirname(__file__), sys.argv[2]))
trainingOutputFile = open(trainingOutputPath, "w")

xmlparser = xmlparser()

for fileName in os.listdir(trainingFolder):
    print(fileName)
    tagsAndVectors = []


    filePath = os.path.abspath(os.path.join(trainingFolder, fileName))
    trainingValues = xmlparser.parse(filePath)

    currentValue = ""
    currentTag = ""
    addingValue = False
    addingTag = False

    previousValue = ""
    tokenLength = 0
    digits = 0
    dictionaryTags = []

    featureVector = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

    #TODO: figure out some way to deal with nested brackets (perhaps a regex)
    for c in trainingValues:
        if c == "(":
            addingValue = True

            if not len(tagsAndVectors) == 0:
                previousValue = tagsAndVectors[len(tagsAndVectors) - 1][10]

            continue

        if addingValue:
            if not c == "[":
                currentValue += c

                tokenLength += 1
                if c.isdigit():
                    digits += 1
            else:
                print(currentValue)
                addingValue = False
                addingTag = True

                #TODO: lexicon lookup here and build feature vector

                currentValue = ""
                continue

        if addingTag:
            if not c == "]":
                currentTag += c
            else:
                print(currentTag + "\n")
                featureVector.append(currentTag)
                tagsAndVectors.append(featureVector)
                currentTag = ""
                featureVector = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
                addingTag = False



arff.dump(trainingOutputPath, tagsAndVectors, relation="Post Office Data")