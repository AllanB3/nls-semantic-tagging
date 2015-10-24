#!/usr/bin/python

import urllib2
import json
import sys
import re

trainingFile = open(sys.argv[1], "w")
trainingMode = sys.argv[2]
trainingData = urllib2.urlopen("http://addressinghistory.edina.ac.uk/ws/search?boundingBox=-3.417,55.867,-2.947,56.021&format=json&maxRows=10000&directory=1905").read()
trainingData = trainingData.replace("\\\'", "")
trainingData = trainingData.replace("\\\"", "")
trainingData = trainingData.replace("\\r", "")
trainingData = trainingData.replace("\\n", "")
trainingData = trainingData.replace("\\", "")
trainingDict = json.loads(trainingData)

for record in trainingDict["results"]:
	for attr in record["properties"]:
		record["properties"][attr] = re.sub(r"(?!([a-z]|[A-Z]))", "", record["properties"][attr])

for record in trainingDict["results"]:
	forename = record["properties"]["forename"]
	if len(forename.split()) is 1 and forename.isalpha():
		if trainingMode == "spelling":
			trainingFile.write(forename.lower() + "\n")
		else:
			trainingFile.write(forename.lower() + "\tforename\n")

	surname = record["properties"]["surname"]
	if len(surname.split()) is 1 and surname.isalpha():
		if trainingMode == "spelling":
			trainingFile.write(surname.lower() + "\n")
		else:
			trainingFile.write(surname.lower() + "\tsurname\n")

	address = record["properties"]["address"]
	if address.strip(",").isalpha():
		if trainingMode == "spelling":
			for word in address.split():
				trainingFile.write(word.lower() + "\n")
		else:
			trainingFile.write(address.lower() + "\taddress\n")