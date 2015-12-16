#!/usr/bin/python

import numpy
from sklearn.naive_bayes import GaussianNB
import os

TRAININGFOLDER = os.path.abspath(os.path.join(os.path.dirname(__file__), "training"))

class tokenClassifier:

    def __init__(self, trainingFile):
        self.trainingFile = open(trainingFile, "r")
        self.gnb = GaussianNB()

    def train(self):
        trainingData = self.trainingFile.read().splitlines()
        dataStart = trainingData.index("@data") + 1

        data = []

        for t in trainingData[dataStart:]:
            data.append(t.split(","))

        dataset = numpy.asanyarray(data)
        trainingValues = dataset[:,:11]
        trainingClasses = dataset[:,11]

        i = 0
        for t in trainingClasses:
            t = t.replace("\'", "")
            if t == "SURNAME":
                trainingClasses[i] = 1
            elif t == "FORENAME":
                trainingClasses[i] = 2
            elif t == "OCCUPATION":
                trainingClasses[i] = 3
            elif t == "WORK_ADDRESS" or t == "HOME_ADDRESS":
                trainingClasses[i] = 4
            else:
                raise ValueError(t + " is not a valid class")
            i += 1

        trainingValues = numpy.array(trainingValues).astype(numpy.int)
        trainingClasses = numpy.array(trainingClasses).astype(numpy.int)
        self.gnb.fit(trainingValues, trainingClasses)

    def classify(self, vector):
        vectorArray = numpy.array(vector).astype(numpy.int)
        predictedClass = self.gnb.predict(vectorArray.reshape(1, -1))

        if predictedClass == 1:
            return "SURNAME"
        elif predictedClass == 2:
            return "FORENAME"
        elif predictedClass == 3:
            return "OCCUPATION"
        elif predictedClass == 4:
            return "ADDRESS"

if __name__ == "__main__":
    training = os.path.abspath(os.path.join(TRAININGFOLDER, "training.arff"))
    c = tokenClassifier(training)
    c.train()
    print(c.classifiy([0,0,0,0,0,7,0,1,0,0,0]))