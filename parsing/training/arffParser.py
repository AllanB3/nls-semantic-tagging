#!/usr/bin/python3

import numpy

"""
Class for parsing ARFF files into NumPy arrays.
"""
class arffParser:

    """
    Static method for parseing an ARFF file.

    :param file: ARFF file to be parsed
    :return: NumPy Array read from ARFF file
    """
    @staticmethod
    def parseFile(file):

        lines = open(file, "r").read().splitlines()
        dataStart = lines.index("@data") + 1

        data = []

        for l in lines[dataStart:]:
            data.append(l.split(","))

        dataset = numpy.asanyarray(data)

        return dataset