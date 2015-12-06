#!/usr/bin/python

import xml.etree.ElementTree as ET
import sys
import os
import importlib

importlib.reload(sys)

class xmlparser:

    def __init__(self):
        pass

    def parseocr(self, xml):
        tree = ET.parse(xml)
        document = tree.getroot()
        text = ""

        for page in document:
            if page.tag == "Page":
                for region in page:
                    if region.tag == "TextRegion":
                        for line in region.findall("Line"):
                            text += line.attrib["text"] + "\n"

        return text

    def parsenls(self, xml):
        tree = ET.parse(xml)
        document = tree.getroot()
        text = ""

        for page in document:
            if page.tag == "page":
                try:
                    text += page.text + "\n"
                except:
                    continue

        return text
