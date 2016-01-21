from collections import defaultdict
import json

from files_handler import writeIntoFile

count = 0

global offset
global count

def byteify(input):
    if isinstance(input, dict):
        return {byteify(key):byteify(value) for key,value in input.iteritems()}
    elif isinstance(input, list):
        return [byteify(element) for element in input]
    elif isinstance(input, unicode):
        return input.encode('utf-8')
    else:
        return input

def list_to_inverted_dict(items):
	d = defaultdict(int)
	for item in items:
	   d[item] += 1
	return d

def create_index():
	#Byteify converts unicode input received from json module
	tokens = byteify(json.load(open("tokens.json", "r")))

	title = list_to_inverted_dict(tokens['title'])
	body = list_to_inverted_dict(tokens['body'])
	infobox = list_to_inverted_dict(tokens['infobox'])
	category = list_to_inverted_dict(tokens['category'])
	external_links = list_to_inverted_dict(tokens['external_links'])
	references = list_to_inverted_dict(tokens['references'])
 	
 	all_words = list(set(title.keys()+text.keys()+infoBox.keys()+category.keys()+externalLink.keys()))

    for key in vocabularyList:
      string = str(count)+' '
      try:
        string += str(round(title[key]/t,4))+' '
      except ZeroDivisionError:
        string += '0.0 '
      try:
        string += str(round(text[key]/b,4))+' '
      except ZeroDivisionError:
        string += '0.0 '
      try:
        string += str(round(infoBox[key]/i,4))+' '
      except ZeroDivisionError:
        string += '0.0 '
      try:
        string += str(round(category[key]/c,4))+' '
      except ZeroDivisionError:
        string += '0.0 '
      try:
        string +=str (round(externalLink[key]/e,4))
      except ZeroDivisionError:
        string += '0.0'
      index[key].append(string)       

    count += 1

    if count%5000==0:
      print count

      offset = writeIntoFile(sys.argv[2], index, dict_Id, countFile,offset)

      index=defaultdict(list)

      dict_Id={}

      countFile+=1
