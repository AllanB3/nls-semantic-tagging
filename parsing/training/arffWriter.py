#!/usr/bin/python

import sys
import os
import arff
import re

path = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(1, path)

from xmlParser import *

trainingFolder = os.path.abspath(os.path.join(os.path.dirname(__file__), sys.argv[1]))
trainingOutputPath = os.path.abspath(os.path.join(os.path.dirname(__file__), sys.argv[2]))
nlsdata = eval(sys.argv[3])
trainingOutputFile = open(trainingOutputPath, "w")

tagsAndVectors = []

xmlparser = xmlparser()

for fileName in os.listdir(trainingFolder):
    filePath = os.path.abspath(os.path.join(trainingFolder, fileName))

    if nlsdata:
        trainingValues = xmlparser.parsenls(filePath)
    else:
        trainingValues = xmlparser.parseocr(filePath)

    matches = re.finditer(r"\([A-Z|a-z|\d|\s|\n|\.|\-|,]*(\s*\n*)\[[A-Z|_]*\]\)", trainingValues, re.M)

    for match in matches:
        token = match.group()
        print(token)
        previousValue = ""
        tokenLength = 0
        digits = 0
        dictionaryTags = []

        featureVector = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

        if len(tagsAndVectors) > 0:
            previousValue = tagsAndVectors[len(tagsAndVectors) - 1][12]

            if previousValue == "SURNAME":
                featureVector[0] = 1
            elif previousValue == "FORENAME":
                featureVector[1] = 1
            elif previousValue == "TITLE":
                featureVector[2] = 1
            elif previousValue == "OCCUPATION":
                featureVector[3] = 1
            elif previousValue == "ADDRESS":
                featureVector[4] = 1

        featureVector[5] = len(re.findall("\d", token))

        tag = re.search(r"\[[A-Z|_]*\]", token).group()
        tag = tag[1 : len(tag) - 1]

        # TODO: change these in annotations
        if tag == "WORK_ADDRESS" or tag == "HOME_ADDRESS":
            tag = "ADDRESS"

        token = re.sub(r"\[(\s|\n)*[A-Z|_]*\]\)", "", token)
        token = re.sub(r"^\(", "", token)
        token = re.sub(r"\d+\s*", "", token)
        print(token)
        featureVector[6] = len(token)

        lexicon = open("classifierTraining.txt", "r").read()
        entries = lexicon.splitlines()

        for e in entries:
            entry, dictTag = e.strip().split("\t")

            if entry == token.lower().strip():
                if dictTag == "surname":
                    featureVector[7] = 1
                elif dictTag == "forename":
                    featureVector[8] = 1
                elif dictTag == "title":
                    featureVector[9] = 1
                elif dictTag == "occupation":
                    featureVector[10] = 1
                elif dictTag == "address":
                    featureVector[11] = 1

        featureVector.append(tag)
        print(featureVector)
        print("")

        tagsAndVectors.append(featureVector)

arffWriter = arff.Writer(trainingOutputPath, relation="postOfficeData", names=['previousSurname',
                                                                               'previousForename',
                                                                               'previousTitle',
                                                                               'previousOccupation',
                                                                               'previousAddress',
                                                                               'tokenLength',
                                                                               'digits',
                                                                               'dictionarySurname',
                                                                               'dictionaryForename',
                                                                               'dictionaryTitle',
                                                                               'dictionaryOccupation',
                                                                               'dictionaryAddress',
                                                                               'class'])

arffWriter.pytypes[str] = '{SURNAME, FORENAME, TITLE, OCCUPATION, ADDRESS}'


for data in tagsAndVectors:
    arffWriter.write(data)