#!/usr/bin/python

from __future__ import division
import os
import sys

gold_standards = open("gold_standards.txt", "r").readlines()
results = {
	"forename": {"true_positive": 0, "true_negative": 0, "false_positive": 0, "false_negative": 0},
	"surname": {"true_positive": 0, "true_negative": 0, "false_positive": 0, "false_negative": 0},
	"address": {"true_positive": 0, "true_negative": 0, "false_positive": 0, "false_negative": 0}
	}

sys.path.insert(1, os.path.abspath(os.path.join(os.path.dirname(__file__), "../parsing/training")))
sys.path.insert(1, os.path.abspath(os.path.join(os.path.dirname(__file__), "../parsing")))

from spellchecker import *
from classifier import *

os.chdir(os.path.join(os.path.dirname(__file__), "../parsing/training"))

spellchecker = SpellChecker("spellcheckerTraining.txt")
spellchecker.train()
classifier = Classifier("classifierTraining.txt")

for g in gold_standards:
	g = g.strip()
	word, actual_tag = g.split("\t", 1)
	corrected_word = spellchecker.correct(word)
	classified_tag = classifier.classify(corrected_word)
	print("Word: " + word)
	print("Expected tag: " + actual_tag)
	print("Corrected word: " + corrected_word)

	if classified_tag:
		if classified_tag == actual_tag:
			results[actual_tag]["true_positive"] += 1

			for key in results:
				if key != actual_tag:
					results[key]["true_negative"] += 1
		else:
			results[actual_tag]["false_negative"] += 1
			results[classified_tag]["false_positive"] += 1

		print("Classified tag: " + classified_tag + "\n")
	else:
		results[actual_tag]["false_negative"] += 1
		print("Classified tag: None\n")

for key in results:
	print(key + ":")
	precision = results[key]["true_positive"] / (results[key]["true_positive"] + results[key]["false_positive"]) * 100
	recall = results[key]["true_positive"] / (results[key]["true_positive"] + results[key]["false_negative"]) * 100
	fscore = (2 * precision * recall) / (precision + recall)

	print("Precision: " + str(precision))
	print("Recall: " + str(recall))
	print("F-score: " + str(fscore) + "\n")