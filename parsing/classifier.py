#!/usr/bin/python

import re

MAXIMUM_EDIT_DISTANCE = 2

class Classifier:

	def __init__(self, dictionaryFile):
		self.dictionary = {}

		dictionaryInput = open(dictionaryFile, "r").read()
		entries = dictionaryInput.splitlines()

		for e in entries:
			key, value = e.split("\t")
			if key in self.dictionary:
				self.dictionary[key].append(value)
			else:
				self.dictionary[key] = [value]

	def getWordsOfEditDistance(self, word, editDistance):
		edits = self.edits(word)

		while editDistance > 1:
			newEdits = []
			for edit in edits:
				newEdits += self.edits(edit)
			edits = set(newEdits)
			editDistance -= 1

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
		return set(w for w in words if w in self.dictionary)

	def classify(self, word, maximumEditDistance=MAXIMUM_EDIT_DISTANCE):
		cleanedWord = re.sub(r"[^a-zA-Z\s]", "", word)

		possibleTags = []
		for value, tag in self.dictionary.iteritems():
			if value == cleanedWord:
				possibleTags = possibleTags + self.dictionary[value]

		try:
			return max(possibleTags, key=possibleTags.count)
		except:
			return ""