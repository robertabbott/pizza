import json
import csv
import codecs

from words import words
from parseData import parseData


class train:

	def __init__ (self, path):
		self.path = path
		self.categories = {}
		self.categoryOccurrences = {'upvotes':[]}
		self.dataset = None
		self.words = None


	def getDataset (self):
		self.dataset = parseData.readDataset(self.path)
		# print self.dataset[0]

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
			
			self.categories[category.split('.')[0]] = cFileList
			self.categoryOccurrences[category.split('.')[0]] = 0

		# print self.categories


	def mapData (self):
		if self.dataset == None:
			return
		else:
			count = 0
			for post in self.dataset[1:2]:
				classification = post['requester_received_pizza']
				text = post['request_text']
				text = self.words.textToList(text)
				textMap = self.words.listToDict (text)

			print textMap
		return 


def main ():
	path = '/Users/robertabbott/Desktop/CS/kaggle/pizza/pizza_request_dataset.json'
	t = train(path)
	t.getDataset ()

	t.getCategories ('/Users/robertabbott/Desktop/CS/kaggle/pizza/code/wordLists/')
	t.mapData ()

main()