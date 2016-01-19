#!/usr/bin/python

import xml.sax
from xml.sax.handler import ContentHandler
import cgi
import re

from nltk.stem.porter import PorterStemmer
from nltk.corpus import stopwords

all_articles = []
stemmer = PorterStemmer()
stop = stopwords.words('english')
	
class Article:
	def __init__(self):
		title = ""
		alternate_links = [] #Alternate representations of title 
		content = ""
		token = {}
		citations = []
		external_links = []
		id = 0

def stem_tokens(tokens, stemmer):
    stemmed = []
    for item in tokens:
    	item = item.encode("utf-8")
    	word = stemmer.stem(item)
    	if word not in stop:
        	stemmed.append(stemmer.stem(item))
    return stemmed

def tokenize(text):
	token = re.sub('[^a-zA-Z0-9 \n\.]', ' ', text)
	token = token.split()
	stems = stem_tokens(token, stemmer)
	return stems

class WikipediaHandler(xml.sax.ContentHandler):
	def __init__(self):
		self.CurrentData = ""
		self.article_no = 0
	
	def get_tokens(self, content, title):
		self.t = title
		self.article.token = {}
		self.article.token['title'] = tokenize(title)
		# self.article.token['text'] = tokenize(get_body(content))
		self.article.token['headings'] = tokenize(self.get_headings(content))
		# self.article.token['References'] = tokenize(get_references(content))
		
	def get_headings(self, text):
		return " ".join([i for i in self.article.headings])

	def startElement(self, tag, attributes):
		"""
		At every <page> parsed, create a new object of class Article
		""" 
		self.CurrentData = tag
		if tag == "page":
			self.article = Article()
			self.article.content = ""
			self.article.id = self.article_no
			self.article_no += 1
			self.article.headings = []

	def characters(self, content):
		"""
		Get content of every header
		"""
		if self.CurrentData == "title":
			self.article.title = content
			
		elif self.CurrentData == "text":		
			self.article.content += content

		#Get headings by comparing with pattern
		content = str(content.encode('utf-8'))
		if content.startswith('==') and content.endswith('=='):
			self.article.headings.append(re.sub('[=]','', content).strip())
			
	def endElement(self, tag):
		
		if self.CurrentData == "text":
			self.get_tokens(self.article.content, self.article.title)

		if tag == "page":
			all_articles.append(Article)
		
		self.CurrentData = ""


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