#!/usr/bin/python

import numpy
from sklearn.naive_bayes import MultinomialNB
import os
import sys

TRAININGFOLDER = os.path.abspath(os.path.join(os.path.dirname(__file__), "training"))
sys.path.append(TRAININGFOLDER)

from arffParser import *

class tokenClassifier:

    def __init__(self, trainingFile):
        self.trainingFile = trainingFile
        self.nb = MultinomialNB()
        self._train()

    def classify(self, vector):
        vectorArray = numpy.array(vector).astype(numpy.int)
        predictedClass = self.nb.predict(vectorArray.reshape(1, -1))

        if predictedClass == 1:
            return "SURNAME"
        elif predictedClass == 2:
            return "FORENAME"
        elif predictedClass == 3:
            return "TITLE"
        elif predictedClass == 4:
            return "OCCUPATION"
        elif predictedClass == 5:
            return "ADDRESS"

    def logProbabilities(self, vector):
        vectorArray = numpy.array(vector).astype(numpy.int)
        probabilities = self.nb.predict_log_proba(vectorArray.reshape(1, -1)).tolist()[0]

        return probabilities

    def _train(self):
        dataset = arffParser.parseFile(self.trainingFile)

        trainingValues = dataset[:,:12]
        trainingClasses = dataset[:,12]

        i = 0
        for t in trainingClasses:
            t = t.replace("\'", "")
            if t == "SURNAME":
                trainingClasses[i] = 1
            elif t == "FORENAME":
                trainingClasses[i] = 2
            elif t == "TITLE":
                trainingClasses[i] = 3
            elif t == "OCCUPATION":
                trainingClasses[i] = 4
            elif t == "WORK_ADDRESS" or t == "HOME_ADDRESS" or t == "ADDRESS":
                trainingClasses[i] = 5
            else:
                raise ValueError(t + " is not a valid class")
            i += 1

        trainingValues = numpy.array(trainingValues).astype(numpy.int)
        trainingClasses = numpy.array(trainingClasses).astype(numpy.int)
        self.nb.fit(trainingValues, trainingClasses)

if __name__ == "__main__":
    training = os.path.abspath(os.path.join(TRAININGFOLDER, "training.arff"))
    c = tokenClassifier(training)
    print(c.classify([0,0,0,0,0,0,6,1,0,0,0,0]))