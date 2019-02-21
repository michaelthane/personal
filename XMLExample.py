#!/usr/env/local python
# -*- coding: utf-8 -*-
import xml.etree.ElementTree as ET
import datetime

### one way to handle is with indexes into the xmlroot
VALUE1, VALUE2, VALUE3, VALUE4 = range(4)

class XMLExample(object):
	"""This object handles XML file access
	"""
	def __init__(self, filename=None):
		"""description
		"""
		self.filename = None;
		if filename:
			self.load(filename)
			self.filename = filename
		else:
		    print("NO file");
			
	def load(self, filename):
		"""Load XML file """
		self.xmltree = ET.parse(filename)
		self.xmlroot = self.xmltree.getroot()   # get root element of the XML tree
		version = self.xmlroot.find('version')
		if version is not None:
			self.version = version.text
		else:
			self.version = 'Version is not in the file'
		ts = self.xmlroot.find('timestamp')
		if ts is not None:
			self.timestamp = ts.text
		else:
			self.timestamp = 'Timestamp is not in the file'
			
		self.block1 = self.xmlroot.find('Block1')

	def save(self):
		"""Save XML file """
		# set timestamp with current time
		filename = self.filename
		ts = self.xmlroot.find('timestamp')
		if ts is not None:
			ts.text = datetime.datetime.now().strftime('%c')
		self.xmltree.write(filename)			# save the XML tree

if __name__ == '__main__':
	limits = XMLExample('ExampleXMLFile.xml')
	print(limits.version)
	print(limits.timestamp)
	print(limits.block1.find('Value1').text)	# example with element search
	print(limits.block1.find('Value2').text)
	print(limits.block1[VALUE3].text)			# example with indexes
	print(limits.block1[VALUE4].text)
	
	# change something....
	limits.block1[VALUE1].text = '100.1'
	
	limits.save()
	