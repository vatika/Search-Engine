#!/usr/bin/python

import xml.sax
from xml.sax.handler import ContentHandler
import cgi

all_article = []

class WikipediaHandler(xml.sax.ContentHandler):
	def __init__(self):
		self.title = ""
		self.CurrentData = ""
	
	def startElement(self, tag, attributes):
		self.CurrentData = tag
    	if tag == "page":
    		article = Article()

	def characters(self, content):
		if self.CurrentData == "title":
			self.title = content
 
	def endElement(self, tag):
		if self.CurrentData == "title":
			article.title = self.title
			print "Title: ", article.title

class Article:
	def __init__(self):
		title = []
		id = ""
		parent_id = ""
		alternate_links = [] #Alternate representations of title 
		content = ""
		tokens = []
		citations = []
		external_links = []


if ( __name__ == "__main__"):
   
   filename = "wiki-search-small.xml"
   # create an XMLReader
   parser = xml.sax.make_parser()
   # turn off namepsaces
   parser.setFeature(xml.sax.handler.feature_namespaces, 0)

   # override the default ContextHandler
   Handler = WikipediaHandler()
   parser.setContentHandler( Handler )
   
   parser.parse(filename)