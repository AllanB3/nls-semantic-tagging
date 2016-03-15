#!/usr/bin/python3

import xml.etree.ElementTree as ET

class XMLParser:

    def __init__(self):
        pass

    @staticmethod
    def parseOCR(xml):
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

    @staticmethod
    def parseNLSDirectory(xml):
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

    @staticmethod
    def parseNLSPage(xml):
        tree = ET.parse(xml)
        document = tree.getroot()
        text = ""

        for line in document:
            if line.tag == "LINE":
                text += line.text + "\n"

        return text

    def parse(self, source, xml):
        if source == "ocr":
            return self.parseOCR(xml)
        elif source == "page":
            return self.parseNLSPage(xml)
        elif source == "directory":
            return  self.parseNLSDirectory(xml)
        else:
            raise IOError("source must equal \"ocr\", \"directory\" or \"page\"")
