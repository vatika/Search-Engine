#!/usr/bin/python

import xml.sax
from xml.sax.handler import ContentHandler
import cgi

all_articles = []


class WikipediaHandler(xml.sax.ContentHandler):
	def __init__(self):
		self.title = ""
		self.CurrentData = ""
		self.article_no = 0
		self.article.content = ""
		
	def get_tokens(self):


	def startElement(self, tag, attributes):
		"""
		At every <page> parsed, create a new object of class Article
		""" 
		self.CurrentData = tag
		if self.CurrentData == "page":
			self.article = Article()
			self.article.id = self.article_no
			self.article_no += 1

	def characters(self, content):
		"""
		Get content of every header
		"""
		if self.CurrentData == "title":
			self.article.title = content

		if self.CurrentData = "text":
			self.article.content = content
			tokens = get_tokens(self.art)
		# if self.CurrentData == "id":
		# 	if content != content:
		# 		self.article.id = int(content)
		# 	else: self.article.id = None

	def endElement(self, tag):
		if self.CurrentData == "title":
			print "Title: ", self.article.title
		# if self.CurrentData == "id":
		# 	print "Id: ", self.article.id
		if self.CurrentData == "page":
			all_articles.append(Article)

class Article:
	def __init__(self):
		title = []
		# id = ""
		# parent_id = ""
		alternate_links = [] #Alternate representations of title 
		content = ""
		tokens = []
		citations = []
		external_links = []
		id = 0


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