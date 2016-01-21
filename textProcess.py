from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer

import re

stemmer = PorterStemmer()
stop = stopwords.words('english')

def stem_tokens(tokens):
    stemmed = []
    for item in tokens:
    	item = item.encode("utf-8")
    	word = stemmer.stem(item)
    	if word not in stop:
        	stemmed.append(stemmer.stem(item))
    return stemmed

def tokenize(text):
	token = re.sub('[^a-zA-Z0-9 \.]', ' ', text)
	token = token.split()
	stems = stem_tokens(token)
	return stems

def remove_stop_words(words):
	filtered_words = []
	for word in words:
		if word not in stop:
			filtered_words.append(word)
	return filtered_words