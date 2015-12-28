#!/usr/bin/python

import os
import sys

TRAININGFOLDER = os.path.abspath(os.path.join(os.path.dirname(__file__), "training"))
sys.path.append(TRAININGFOLDER)

from tokenClassifier import *
from arffParser import *
from nltk.probability import ConditionalFreqDist
from nltk.probability import ConditionalProbDist
from nltk.probability import LidstoneProbDist
import re
from math import log
from xmlParser import *
import string

class hiddenMarkovModel:

    def __init__(self, trainingData=TRAININGFOLDER+"/training.arff", lexicon=TRAININGFOLDER+"/classifierTraining.txt"):
        self.trainingData = trainingData
        self.lexicon = open(lexicon, "r").read().splitlines()
        self.sensorModel = None
        self.transitionModel = None
        self.states = ["SURNAME", "FORENAME", "TITLE", "OCCUPATION", "ADDRESS"]
        self._train()

    def tag(self, text):
        text = text.translate(str.maketrans(string.punctuation, "                                "))
        text = text.replace("\n", " ")
        tokens = text.split()
        tokensAndVectors = []

        for t in tokens:
            featureVector = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
            featureVector[5] = len(re.findall("\d", t))
            featureVector[6] = len(t)
            tokensAndVectors.append((t, featureVector))

        return self._viterbi(tokensAndVectors)

    def _train(self):
        self.sensorModel = tokenClassifier(self.trainingData)

        dataset = arffParser.parseFile(self.trainingData)
        transitions = [("<s>", dataset[0][12]), ("</s>", dataset[len(dataset) - 1][12])]

        for i in range(0, len(dataset) - 1):
            tag = dataset[i][12]
            tokenLength = int(dataset[i][6])

            j = 0
            while j < tokenLength:
                transitions.append((tag, tag))
                j += 1

            transitions.append((tag, dataset[i + 1][12]))

        transitionFreqDist = ConditionalFreqDist(transitions)
        self.transitionModel = ConditionalProbDist(transitionFreqDist, LidstoneProbDist, 0.01, bins=3125)

    def _viterbi(self, tokensAndVectors):
        viterbi = []
        backpointers = []

        firstViterbi = {}
        firstBackpointer = {}
        token, featureVector = tokensAndVectors[0]

        for l in self.lexicon:
            entry, dictTag = l.strip().split("\t")
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

        for i in range(0, len(self.states)):
            firstViterbi[self.states[i]] = ((0 - log(self.transitionModel["<s>"].prob(self.states[i]))) + (self.sensorModel.logProbabilities(featureVector)[i]))
            firstBackpointer[self.states[i]] = "<s>"

        viterbi.append(firstViterbi)
        backpointers.append(firstBackpointer)

        index = 0
        for t in range(1, len(tokensAndVectors)):
            nextViterbi = {}
            nextBackpointer = {}
            token, featureVector = tokensAndVectors[t]

            for l in self.lexicon:
                entry, dictTag = l.strip().split("\t")
                if token.lower().strip() in entry.split():
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

            for i in range(0, len(self.states)):
                previousTag = min(viterbi[index], key=lambda state : viterbi[index].get(state) + (0 - log(self.transitionModel[self.states[i]].prob(self.states[i]))))

                if previousTag == "SURNAME":
                    featureVector[0] = 1
                elif previousTag == "FORENAME":
                    featureVector[1] = 1
                elif previousTag == "TITLE":
                    featureVector[2] = 1
                elif previousTag == "OCCUPATION":
                    featureVector[3] = 1
                elif previousTag == "ADDRESS":
                    featureVector[4] = 1

                nextViterbi[self.states[i]] = min([viterbi[index][s] + (0 - log(self.transitionModel[s].prob(self.states[i]))) + (0 - self.sensorModel.logProbabilities(featureVector)[i]) for s in self.states])
                nextBackpointer[self.states[i]] = previousTag

                featureVector[0:5] = [0, 0, 0, 0, 0]

            viterbi.append(nextViterbi)
            backpointers.append(nextBackpointer)
            index += 1

        lastViterbi = {}
        for s in self.states:
            lastViterbi[s] = 0

        lastViterbi["</s>"] = min([viterbi[index][s] + (0 - log(self.transitionModel[s].prob("</s>"))) for s in self.states])

        lastBackpointer = {}
        for s in self.states:
            lastBackpointer[s] = min(viterbi[index], key=lambda state : viterbi[index][state] + (0 - log(self.transitionModel[s].prob("</s>"))))

        viterbi.append(lastViterbi)
        backpointers.append(lastBackpointer)

        tags = []
        tokenIndex = 0
        for i in range(1, len(backpointers)):
            for s in self.states:
                if s == min(viterbi[i], key=viterbi[i].get):
                    tags.append((tokensAndVectors[tokenIndex][0], backpointers[i][s]))
            tokenIndex += 1

        return tags

if __name__ == "__main__":
    h = hiddenMarkovModel()

    x = xmlParser()
    text = x.parseNLSPage("training/hmmTestingData/84017556.8.xml")

    for token in h.tag(text):
        print(token)