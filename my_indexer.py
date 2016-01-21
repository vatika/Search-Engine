from collections import defaultdict
import json

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
	print tokens