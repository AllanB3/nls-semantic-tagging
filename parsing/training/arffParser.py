#!/usr/bin/python3

import numpy

class arffParser:

    @staticmethod
    def parseFile(file):

        lines = open(file, "r").read().splitlines()
        dataStart = lines.index("@data") + 1

        data = []

        for l in lines[dataStart:]:
            data.append(l.split(","))

        dataset = numpy.asanyarray(data)

        return dataset