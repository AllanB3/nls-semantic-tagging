#!/usr/bin/python3

import xml.etree.ElementTree as ET
import sys

"""
Class for parsing XML transcripts of Post Office directories from a variety of sources. Possible sources are:
    "ocr": transcript from the supplied OCR script
    "page": a transcript of a single page from the National Library of Scotland
    "directory": a transcript of a whole directory from the National Library of Scotland

To use, first create an XMLParser object like so:
    from xmlParser import *
    parser = XMLParser()
and then call:
    parser.parse(source, /path/to/xml)

Can also be write text transcript to a file via the command line:
    python3 xmlParser.py /path/to/xml /path/to/output
"""
class XMLParser:

    def __init__(self):
        pass

    """
    Static private method for parsing transcripts from the OCR module.

    :param xml: Path to XML transcript
    :return: text transcript
    """
    @staticmethod
    def _parseOCR(xml):
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

    """
    Static private method for parsing transcripts of whole directories from the National Library of Scotland.

    :param xml: Path to XML transcript
    :return: text transcript
    """
    @staticmethod
    def _parseNLSDirectory(xml):
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

    """
    Static private method for parsing transcripts of single pages from the National Library of Scotland.

    :param xml: Path to XML transcript
    :return text transcript
    """
    @staticmethod
    def _parseNLSPage(xml):
        tree = ET.parse(xml)
        document = tree.getroot()
        text = ""

        for line in document:
            if line.tag == "LINE":
                text += line.text + "\n"

        return text

    """
    Method for parsing transcripts from each of the three available sources.

    :param source: Source of transcript
    :param xml: Path to XML transcript
    :return: text transcript
    :raises: IOError
    """
    def parse(self, source, xml):
        if source == "ocr":
            return self._parseOCR(xml)
        elif source == "page":
            return self._parseNLSPage(xml)
        elif source == "directory":
            return  self._parseNLSDirectory(xml)
        else:
            raise IOError("source must equal \"ocr\", \"directory\" or \"page\"")

if __name__ == "__main__":
    xmlParser = XMLParser()
    print(xmlParser.parse(sys.argv[1], sys.argv[2]))
