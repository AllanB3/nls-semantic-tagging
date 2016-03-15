#!/usr/bin/python3

import sys
import os
import arff
import re
import string
import hashlib

path = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(1, path)

TRAINING_FOLDER = "training"
ARFF_FILE = "training.arf"

from xmlParser import *

"""
Class for extracting features from training transcripts or BRAT annotations. At present does not handle NLS directory
transcripts.

Annotated tokens in XML must be of the form:
    (token [TAG])

To use:
    from featureExtractor import *
    extractor = FeatureExtractor()
    extractor.extractFeatures()

Can also be run from the command line:
    python3 featureExtractor.py

:param trainingFolder: Directory of training transcripts/BRAT annotations.
:param outputPath: Path to ARFF training file
"""
class FeatureExtractor:

    def __init__(self, trainingFolder=TRAINING_FOLDER, outputPath=ARFF_FILE):
        self.trainingFolder = trainingFolder
        self.outputPath = outputPath
        self.xmlparser = XMLParser()

    """
    A method which extracts features from our training transcripts/BRAT annotations.
    """
    def extractFeatures(self):
        tagsAndVectors = []

        for fileName in os.listdir(self.trainingFolder):
            filePath = os.path.abspath(os.path.join(self.trainingFolder, fileName))

            if fileName[-3:] == "xml":
                # TODO: have this handle whole directories from NLS
                if fileName[:4] == "SPOD":
                    trainingValues = self.xmlparser.parse("ocr", filePath)
                else:
                    trainingValues = self.xmlparser.parse("page", filePath)

                annotations = re.finditer(r"\([A-Z|a-z|\d|\s|\n|\.|\-|,]*(\s*\n*)\[[A-Z|_]*\]\)", trainingValues, re.M)
                matches = []

                for a in annotations:
                    word, tag = a.group().split("[")
                    words = word.split(",")
                    tag = tag.translate(str.maketrans(string.punctuation, "                                ")).replace(" ", "")

                    for i in range(0, len(words)):
                        matches.append((words[i].translate(str.maketrans(string.punctuation, "                                ")), tag))

                for match in matches:
                    token, tag = match
                    print(token)

                    featureVector = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

                    if len(tagsAndVectors) > 0:
                        previousValue = tagsAndVectors[len(tagsAndVectors) - 1][13]

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
                    featureVector[6] = len(token)

                    lexicon = open("classifierTraining.txt", "r").read()
                    entries = lexicon.splitlines()

                    for e in entries:
                        entry, dictTag = e.strip().split("\t")

                        if hashlib.md5(token.lower().lstrip().strip().replace(string.digits, "          ").encode("utf-8")).hexdigest() == entry:
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

                    featureVector[12] = len([c for c in token if c.isupper()])

                    featureVector.append(tag)
                    print(featureVector)
                    print("")

                    tagsAndVectors.append(featureVector)
            elif fileName[-3:] == "ann":
                lines = open(filePath, "r").read().splitlines()

                entries = {}
                tokens = {}

                for l in lines:
                    key, value = l.split("\t", 1)

                    if key[0] == "E":
                        entries[key] = value
                    else:
                        tokens[key] = value

                for key, entry in entries.items():
                    constituentTokens = entry.split()

                    for c in constituentTokens:
                        tag, index = c.split(":")
                        tokenData, token = tokens[index].split("\t")
                        print(token)

                        for t in token.split(","):
                            featureVector = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

                            if len(tagsAndVectors) > 0:
                                previousValue = tagsAndVectors[len(tagsAndVectors) - 1][13]

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

                            featureVector[5] = len(re.findall(r"\d", t))
                            featureVector[6] = len(t)

                            lexicon = open("classifierTraining.txt", "r").read().splitlines()

                            for l in lexicon:
                                entry, dictTag = l.split("\t")

                                if hashlib.md5(token.lower().lstrip().strip().replace(string.digits, "          ").encode("utf-8")).hexdigest() == entry:
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

                            featureVector[12] = len([c for c in token if c.isupper()])

                            if tag == "POD_entry":
                                tag = "SURNAME"

                            featureVector.append("".join([c for c in tag.upper() if not c.isdigit()]))
                            print(featureVector)
                            print("")

                            tagsAndVectors.append(featureVector)
            else:
                raise IOError("The file " + fileName + " is in an unsupported format. Please use .xml or .ann files.")

        arffWriter = arff.Writer(self.outputPath, relation="postOfficeData", names=['previousSurname',
                                                                                       'previousForename',
                                                                                       'previousTitle',
                                                                                       'previousOccupation',
                                                                                       'previousAddress',
                                                                                       'digits',
                                                                                       'tokenLength',
                                                                                       'dictionarySurname',
                                                                                       'dictionaryForename',
                                                                                       'dictionaryTitle',
                                                                                       'dictionaryOccupation',
                                                                                       'dictionaryAddress',
                                                                                       'capitalLetters',
                                                                                       'class'])

        arffWriter.pytypes[str] = '{SURNAME, FORENAME, TITLE, OCCUPATION, ADDRESS}'

        for data in tagsAndVectors:
            arffWriter.write(data)

if __name__ == "__main__":
    f = FeatureExtractor()
    f.extractFeatures()
