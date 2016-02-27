#!/usr/bin/python3

import xml.etree.ElementTree as ET

class xmlParser:

    def __init__(self):
        pass

    def parseOCR(self, xml):
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

    def parseNLSDirectory(self, xml):
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

    def parseNLSPage(self, xml):
        tree = ET.parse(xml)
        document = tree.getroot()
        text = ""

        for line in document:
            if line.tag == "LINE":
                text += line.text + "\n"

        return text