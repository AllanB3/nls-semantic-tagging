#!/usr/bin/python3

from hiddenMarkovModel import *
from xmlParser import *
import rdflib
from rdflib.namespace import RDF
import pathlib
import os

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
		nextTags = {"SURNAME": ["FORENAME", "TITLE"], "FORENAME": ["OCCUPATION", "ADDRESS"], "TITLE": ["FORENAME", "OCCUPATION", "ADDRESS"], "OCCUPATION": ["OCCUPATION", "ADDRESS"], "ADDRESS": ["ADDRESS"]}
		entry = {}
		previousTag = "SURNAME"
		for token, tag in tokensAndTags:
			if not tag in nextTags[previousTag]:
				entries.append(entry)
				entry = {}

				if not tag == "SURNAME":
					continue

			if not tag in entry:
				entry[tag] = token.lstrip().strip()
			else:
				entry[tag] = entry[tag] + ", "  + token.lstrip().strip()

			previousTag = tag

		return entries

	@staticmethod
	def addRecordsToDatabase(records, recordYear):
		g = rdflib.Graph()
		schema = rdflib.Namespace("http://schema.org/")
		person = rdflib.Namespace("http://schema.org/Person#")

		try:
			data = open("../{0}.ttl".format(recordYear), "r").read()
			g.load(data)
		except FileNotFoundError:
			pass

		uri = pathlib.Path(os.path.abspath(os.path.join(os.path.dirname(__file__),
														"../database/{0}.ttl".format(recordYear)))).as_uri()

		idNumber = 0
		for r in records:
			idNumber += 1
			identifier = rdflib.URIRef("{0}#{1}".format(uri, idNumber))
			g.add((identifier, RDF.type, schema.Person))
			for key, value in r.items():
				if key == "SURNAME":
					relation = person.familyName
				elif key == "FORENAME":
					relation = person.givenName
				elif key == "TITLE":
					relation = person.honorificPrefix
				elif key == "OCCUPATION":
					relation = person.jobTitle
				elif key == "ADDRESS":
					relation = person.address
				else:
					raise ValueError("{0} is not a valid key".format(key))

				g.add((identifier, relation, rdflib.Literal(value)))

		g.serialize(uri, format="turtle")


if __name__ == "__main__":
	e = EntryExtractor()
	entries = e.extractFeatures("training/hmmDevTest/1911-12-p96/84311938.8.xml", "page")
	e.addRecordsToDatabase(entries, "1911")
