#!/usr/bin/python

import xml.etree.ElementTree as ET
import sys

reload(sys)  
sys.setdefaultencoding('utf8')

tree = ET.parse(sys.argv[1])
document = tree.getroot()

for page in document:
	if page.tag == "Page":
		for region in page:
			if region.tag == "TextRegion":
				for line in region.findall("Line"):
					print(line.attrib["text"])