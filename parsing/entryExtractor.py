##!/usr/bin

from hiddenMarkovModel import *
from xmlParser import *

class EntryExtractor:

	def __init__(self):
		self.xmlParser = xmlParser()
		self.hiddenMarkovModel = hiddenMarkovModel()

	def extractFeatures(self, filePath, source):
		if source == "ocr":
			text = self.xmlParser.parseOCR(filePath)
		elif source == "page":
			text = self.xmlParser.parseNLSPage(filePath)
		elif source == "directory":
			text = self.xmlParser.parseNLSDirectory(filePath)
		else:
			raise IOError("source must equal \"ocr\", \"directory\" or \"page\"")

		tokensAndTags = self.hiddenMarkovModel.tag(text)

		entries = []
		nextTags = {"SURNAME": ["FORENAME", "TITLE"], "FORENAME": ["OCCUPATION", "ADDRESS"], "TITLE": ["FORENAME", "OCCUPATION", "ADDRESS"], "OCCUPATION": ["ADDRESS"], "ADDRESS": ["ADDRESS"]}
		entry = {}
		previousTag = "SURNAME"
		for token, tag in tokensAndTags:
			if not tag in nextTags[previousTag]:
				print(entry)
				entries.append(entry)

				entries = []
				entry = {}

				if not tag == "SURNAME":
					continue

			if not tag in entry:
				entry[tag] = token
			else:
				entry[tag] = entry[tag] + ", "  + token

			previousTag = tag

		return entries

if __name__ == "__main__":
	e = EntryExtractor()
	entries = e.extractFeatures("training/hmmDevTest/1911-12-p96/84311938.8.xml", "page")
