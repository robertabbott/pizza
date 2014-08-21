# word processing for train


import re
from collections import defaultdict

class words:
	def __init__ (self, stopwords):
		self.commonWords = stopwords

	def cleanUpWord(self, word):
		word = word.lower()
		if (len(word) < 2):
			return None
		elif (word.isdigit()):
			return None
		elif (word in self.commonWords):
			return None
		
		return word

	def listToDict (self, l):
		d = defaultdict(int)
		self.addListToDict(l, d)
		return d

	def addListToDict (self, l, d):
		for word in l:
			d[word] += 1

	def textToList (self, text):
		cleanedWords = map(self.cleanUpWord, re.split('\W+', text.strip()))
		return filter(lambda word : word and (len(word) > 0), cleanedWords)