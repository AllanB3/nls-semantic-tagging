#!/usr/bin/python

import collections
import re

MAXIMUM_EDIT_DISTANCE = 2

class SpellChecker:

	def __init__(self,trainingFile):
		self.trainingFile = trainingFile

	def train(self):
		trainingData = open(self.trainingFile, "r").read().lower()
		model = collections.defaultdict(lambda: 1)
		for t in trainingData:
			model[t] += 1
		self.model = model

	def getWordsOfEditDistance(self, word, editDistance):
		edits = self.edits(word)

		while editDistance > 1:
			newEdits = []
			for edit in edits:
				newEdits += edits(edit)
			edits = set(newEdits)

		return edits

	def edits(self, word):
		alphabet = 'abcdefghijklmnopqrstuvwxyz'
		s = [(word[:i], word[i:]) for i in range(len(word) + 1)]
		deletes = [a + b[1:] for a, b in s if b]
		transposes = [a + b[1] + b[0] + b[2:] for a, b in s if len(b) > 1]
		replaces = [a + c + b[1:] for a,b in s for c in alphabet if b]
		inserts = [a + c + b for a,b in s for c in alphabet]
		return set(deletes + transposes + replaces + inserts)

	def known(self, words):
		return set(w for w in words if w in self.model)

	def correct(self, word, maximumEditDistance=MAXIMUM_EDIT_DISTANCE):
		word = re.sub(r'(?!([a-z]|\d))', '', word.lower())
		candidates = self.known([word]) or [word]

		while maximumEditDistance > 0:
			candidates.union(self.known(self.getWordsOfEditDistance(word, maximumEditDistance)))
			maximumEditDistance -= 1

		return max(candidates, key=self.model.get)