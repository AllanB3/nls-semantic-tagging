#!/usr/bin/python3

import os
import rdflib

DATABASE = os.path.abspath(os.path.join(os.path.dirname(__file__), "../database"))

class DatabaseQuerier:

    def __init__(self, databaseDirectory=DATABASE):
        self.graph = rdflib.Graph()

        for fileName in os.listdir(databaseDirectory):
            filePath = os.path.abspath(os.path.join(DATABASE, fileName))
            self.graph.parse(filePath)
