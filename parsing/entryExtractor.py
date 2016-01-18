#!/usr/bin

from hiddenMarkovModel import *
from xmlParser import *

class EntityExtractor:

	def __init__(self):
		self.xmlParser = xmlParser()
		self.hiddenMarkovModel = HiddenMarkovModel()

	def extractFeatures(self, filePath, source):
		xmlData = open(filePath, "").read()

		if source == "ocr":
			text = self.xmlParser.parseOCR(xmlData)
		elif source == "page":
			text = self.xmlParser.parseNLSPage(xmlData)
		elif source == "directory":
			text = self.xmlParser.parseNLSDirectory(xmlData)
		else:
			raise IOError("source must equal \"ocr\", \"directory\" or \"page\"")

		tokensAndTags = self.hiddenMarkovModel.tag(text)

		entries = []
		nextTags = {"SURNAME": ["FORENAME", "TITLE"], "FORENAME": ["OCCUPATION", "ADDRESS"], "TITLE": ["FORENAME", "OCCUPATION", "ADDRESS"], "OCCUPATION": ["ADDRESS"], "ADDRESS": ["ADDRESS"]}
		entry = {}
		previousTag = "SURNAME"
		for token, tag in tokensAndTags:
			if not tag in nextTags[previousTag]:
				if tag == "SURNAME":
					entries.append(entry)

				entries = []
				nextTags = ["SURNAME"]
				entry = {}

				if not tag == "SURNAME":
					continue

			entry[tag] = token
			previousTag = tag

		return entries
