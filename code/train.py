import json
import csv
import codecs

from words import words
from parseData import parseData
from collections import defaultdict


class train:

	def __init__ (self, path):
		self.dataset = parseData.readDataset (path)
		self.wordCount = defaultdict (int)
		self.wordOccurrenceCount = defaultdict (int)


	def getCategories (self, filename):
		categories = []
		categoriesFile = open(filename+'categories.txt','r')
		for line in categoriesFile:
			categories.append (line)

		for category in categories:
			if '\n' in category:
				category = category[:len(category)-1]
			cFile = open (filename+category, 'r')
			cFileList = []
			for line in cFile:
				if '\n' in line:
					line = line[:len(line)-1]
				if '\r' in line:
					line = line[:len(line)-1]
				cFileList.append (line)

			if category == 'stopwords.txt':
				self.words = words (cFileList)

			categories = {}
			categories[category.split('.')[0]] = cFileList
			categories['stopwords'] = self.words.listToDict(categories['stopwords'])
			# self.categoryOccurrences[category.split('.')[0]] = 0

			return categories

		# print self.categories


	def mapData (self):
		categories = self.getCategories ('/Users/robertabbott/Desktop/CS/kaggle/pizza/code/wordLists/')
		if self.dataset == None:
			return
		else:
			count = 0
			tWordList = []
			fWordList = []
			for post in self.dataset:
				classification = post['requester_received_pizza']
				if classification == True:
					tWordList += self.words.textToList(post['request_text'])
				else:
					fWordList += self.words.textToList(post['request_text'])

				

			textMapT = self.words.listToDict (tWordList)
			textMapF = self.words.listToDict (fWordList)


			for word in textMapT.keys():
				if categories['stopwords'][word] != 1:
					self.wordCount[word] += textMapT[word]
					self.wordOccurrenceCount[word] += textMapT[word]

			for word in textMapF.keys():
				if categories['stopwords'][word] != 1:
					self.wordCount[word] -= textMapF[word]
					self.wordOccurrenceCount[word] += textMapF[word]

			print self.wordCount
			print self.wordOccurrenceCount
		return 


def main ():
	path = '/Users/robertabbott/Desktop/CS/kaggle/pizza/pizza_request_dataset.json'
	t = train(path)
	t.mapData ()

main()








