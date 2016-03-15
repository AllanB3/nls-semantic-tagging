#!/usr/bin/python3

import os
import collections
import re
import sys

TRAININGFILE = os.path.abspath(os.path.join(os.path.dirname(__file__), "training/spellcheckerTraining.txt"))
MAXIMUM_EDIT_DISTANCE = 2

"""
A spell checker which uses the concept of edit distance of each possible correction from a word and the frequency of
those corrections to choose the most likely correction of a word.

Can be used from the command line:
    python3 spellChecker.py /path/to/input /path/to/output

:param trainingFile: File of lexicon of training words
"""
class SpellChecker:

    def __init__(self,trainingFile=TRAININGFILE):
        self.trainingFile = trainingFile
        trainingData = open(self.trainingFile, "r").read().lower()
        model = collections.defaultdict(lambda: 1)
        for t in trainingData.splitlines():
            model[t] += 1
        self.model = model

    """
    Method for getting corrections the minimum edit distance away from a word up to a maximum edit distance.

    :param word: Word to correct
    :param editDistance: Maximum edit distance to search to
    :return: A list of corrections the minimum possible edit distance away
    """
    def getWordsOfEditDistance(self, word, editDistance):
        edits = self.edits(word)

        while editDistance > 1:
            newEdits = []
            for edit in edits:
                newEdits += self.edits(edit)

            if len(self.known(edits)) != 0:
                edits = self.known(edits)
            else:
                self.known(set(newEdits))

            editDistance -= 1

        return edits

    """
    Method for returning all possible corrections an edit distance of 1 away from a word.

    :param word: Word to find corrections for
    :return: Set of possible corrections an edit distance of 1 away from word
    """
    def edits(self, word):
        alphabet = 'abcdefghijklmnopqrstuvwxyz'
        s = [(word[:i], word[i:]) for i in range(len(word) + 1)]
        deletes = [a + b[1:] for a, b in s if b]
        transposes = [a + b[1] + b[0] + b[2:] for a, b in s if len(b) > 1]
        replaces = [a + c + b[1:] for a,b in s for c in alphabet if b]
        inserts = [a + c + b for a,b in s for c in alphabet]
        return set(deletes + transposes + replaces + inserts)

    """
    Returns the set of known words in a list of words.

    :param words: List of words to find known words for
    :return: List of known words
    """
    def known(self, words):
        return set(w for w in words if w in self.model)

    """
    Method for finding best correction for a word.

    :param word: Word to correct
    :param maximumEditDistance: Maximum edit distance to search to
    :return: Best correction for word
    """
    def correct(self, word, maximumEditDistance=MAXIMUM_EDIT_DISTANCE):
        cleanedWord = re.sub(r'[^0-9a-zA-Z\s]', '', word.lower())

        if cleanedWord.isdigit():
            return cleanedWord

        candidates = {cleanedWord}

        candidates = self.known(candidates.union(self.getWordsOfEditDistance(cleanedWord, maximumEditDistance)))

        if len(candidates) > 0:
            return max(candidates, key=self.model.get)
        else:
            return word

    """
    Method for correcting a text file and outputting the result to another text file.

    :param inputPath: /path/to/input/file
    :param outputPath: /path/to/output/file
    """
    def spellcheck(self, inputPath, outputPath):
        words = open(inputPath, "r").read().splitlines()
        outputFile = open(outputPath, "w")

        for line in words:
            for word in line.split(" "):
                if "," in word:
                    outputFile.write(self.correct(word) + ", ")
                else:
                    outputFile.write(self.correct(word) + " ")
            outputFile.write("\n")

if __name__ == "__main__":
    spellChecker = SpellChecker()
    spellChecker.spellcheck(sys.argv[1], sys.argv[2])
