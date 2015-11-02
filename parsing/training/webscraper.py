#!/usr/bin/python

import urllib2
import json
import sys
import re
import string

trainingFile = open(sys.argv[2], "w")
trainingMode = sys.argv[1]
trainingData = urllib2.urlopen("http://addressinghistory.edina.ac.uk/ws/search?boundingBox=-3.417,55.867,-2.947,56.021&format=json&maxRows=10000&directory=1905").read()
trainingData = trainingData.replace("\\\'", "")
trainingData = trainingData.replace("\\\"", "")
trainingData = trainingData.replace("\\r", "")
trainingData = trainingData.replace("\\n", "")
trainingData = trainingData.replace("\\", "")
trainingDict = json.loads(trainingData)

punctuation = re.compile("[%s]" % re.escape(string.punctuation))
for record in trainingDict["results"]:
	for attr in record["properties"]:
		record["properties"][attr] = punctuation.sub("", record["properties"][attr])

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

	occupation = record["properties"]["profession"]
	if occupation.isalpha():
		if trainingMode == "spelling":
			for word in occupation.lower().split():
				trainingFile.write(word)
		else:
			trainingFile.write(occupation.lower() + "\toccupation\n")

addresses = open("streets.txt", "r").read().splitlines()
for address in addresses:
	if trainingMode == "spelling":
		for word in address.lower().split():
			trainingFile.write(word)
	else:
		trainingFile.write(address.lower() + "\taddress\n")