#!/usr/bin/python3

from sklearn.naive_bayes import BernoulliNB
import os
import sys

TRAININGFOLDER = os.path.abspath(os.path.join(os.path.dirname(__file__), "training"))
sys.path.append(TRAININGFOLDER)

from arffParser import *

"""
Class which uses a Bernoulli naive Bayes classifier which is used for the sensor model of the hidden Markov model.

:param traningFile: Path to ARFF training file
"""
class tokenClassifier:

    def __init__(self, trainingFile):
        self.trainingFile = trainingFile
        self.nb = BernoulliNB()
        self._train()

    """
    Method which classifies a single token as a surname, forename, title, occupation, or address.

    :param vector: Feature vector of token to be classified
    :return: Predicted class of feature vector
    """
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

    """
    Method which returns the log probabilities of a single token being in each class.

    :param vector: Feature vector of token
    :return: A list of the probabilities of being a surname, forename, title, occupation or address respectively
    """
    def logProbabilities(self, vector):
        vectorArray = numpy.array(vector).astype(numpy.int)
        probabilities = self.nb.predict_log_proba(vectorArray.reshape(1, -1)).tolist()[0]

        return probabilities

    """
    A private method for training the naive Bayes classifier.
    """
    def _train(self):
        dataset = arffParser.parseFile(self.trainingFile)

        trainingValues = dataset[:,:13]
        trainingClasses = dataset[:,13]

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
