#!/usr/bin/python

import xml.sax
from xml.sax.handler import ContentHandler
import cgi
import timeit

from textProcess import stem_tokens, remove_stop_words, tokenize

import re

all_articles = []

ext_headers = ['references','external links', 'further reading', 'see also']

class Article:
	def __init__(self):
		title = ""
		alternate_links = [] #Alternate representations of title 
		content = ""
		token = {}
		citations = []
		external_links = []
		id = 0

def processTitle(title):
	"""
	Title is converted to lower case, tokenized and stemmed
	"""
	return stem_tokens(tokenize(data.lower()), stemmer)    


class WikipediaHandler(xml.sax.ContentHandler):
	def __init__(self):
		self.ext_tag = 0
		self.CurrentData = ""
		self.article_no = 0
	
	def get_tokens(self, content, title):
		self.article.token['title'] = tokenize(title)
		# self.article.token['text'] = tokenize(get_body(content))
		self.article.token['headings'] = tokenize(self.get_headings(content))
		self.article.token['References'] = tokenize(get_references(content))
	
	def get_headings(self, text):
		return " ".join([i for i in self.article.headings])

	def get_references( self, content):
		"""
		Filter content by removing all references and external links
		"""
		content = re.sub( '\n', ' ', content)
		ref = re.findall( "<ref.*?</ref>", content)
		self.article.token['References'] = []
		for i in ref:
			i = re.sub("<ref.*?>", '', i)
			i = re.sub( "</ref>", '', i)
			self.article.token['References'].append(i)
		content = re.sub("<ref.*?</ref>", ' ', content)
		content = re.sub("i.e", '', content)
		content = re.sub("\.", ' ', content)
		content = re.sub('[^a-zA-Z0-9 ]', '', content)
		content = re.sub(' +', ' ', content)
		content = content.split()
		#words ki numbering yaad rakhna oreder needed :P

		#now content is list of words in the body
		#removed references , links, duplicates, etc
		self.article.content = content



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
			self.article.token = {}
			self.article.token['Category'] = []
			self.article.token['external_links'] = []

	def deal(self, content):
		if content == "further reading" :
			self.ext_tag = 3
		elif content == "see also" :
			self.ext_tag = 4
		elif content == "references" :
			self.ext_tag = 1
	
	def extract_external_links(self, content):
		lines=content.split("\n")
		for i in xrange(len(lines)):
			if '* [' in lines[i] or '*[' in lines[i]:
				word=""
				temp=lines[i].split(' ')
				word=[key for key in temp if 'http' not in temp]
				try:
					word=' '.join(word).encode('utf-8')
					self.article.token['external_links'].extend(remove_stop_words(stem_tokens(tokenize(word))))
				except:
					pass
					
	def characters(self, content):
		"""
		Get content of every header
		"""

		content = str(content.encode('utf-8')).lower()

		if self.CurrentData == "title":
			self.article.title = content
		
		elif content.startswith('[[category:' ):
			content = re.sub('category:', '', content)
			content = re.sub('[^a-zA-Z0-9 ]', '', content)
			self.article.token['Category'].append( content)
		
		elif content.startswith('==') and content.endswith('=='):
			content = (re.sub("=+", '', content )).strip()
			if content in ext_headers :
				self.deal(content)
			else:
				self.ext_tag = 0
				self.article.headings.append(re.sub("=+", '', content).strip())

		elif 'http' in content and self.article_no > 1:
			self.extract_external_links(content)

		elif self.CurrentData == "text":	
			self.article.content += content

		#Get headings by comparing with pattern
			
	def endElement(self, tag):
		if self.CurrentData == "text":

#			do not know use of this neeche
			self.get_tokens(self.article.content, self.article.title)
			print self.article.token['Category']
		if tag == "page":
			all_articles.append(Article)
		
		self.CurrentData = ""

def main():

   #filename = "wiki-search-small.xml"
   filename = "./chota.xml"
   # create an XMLReader
   parser = xml.sax.make_parser()
   # turn off namepsaces
   parser.setFeature(xml.sax.handler.feature_namespaces, 0)

   # override the default ContextHandler
   Handler = WikipediaHandler()
   parser.setContentHandler( Handler )
   
   parser.parse(filename)


if ( __name__ == "__main__"):
   
	start = timeit.default_timer()
	main()
	stop = timeit.default_timer()
	print stop - start