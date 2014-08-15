import json
import csv
import codecs

from parseData import parseData


class train:

	def __init__ (self, path):
		self.path = path
		self.categories = {}
		self.categoryOccurrences = {'upvotes':[]}
		self.dataset = None


	def getDataset (self):
		self.dataset = parseData.readDataset(self.path)
		# print self.dataset[0]

	def getCategories (self, filename):
		categories = []
		categoriesFile = open(filename,'r')
		for line in categoriesFile:
			categories.append (line)

		for category in categories:
			if '\n' in category:
				category = category[:len(category)-1]
			cFile = open (category, 'r')
			cFileList = []
			for line in cFile:
				if '\n' in line:
					line = line[:len(line)-1]
				if '\r' in line:
					line = line[:len(line)-1]
				cFileList.append (line)
			
			self.categories[category.split('.')[0]] = cFileList
			self.categoryOccurrences[category.split('.')[0]] = 0

		# print self.categories


	def mapDataByCategory (self):
		if self.dataset == None:
			return
		else:
			count = 0
			for post in self.dataset:
				classification = post['requester_received_pizza']
				text = post['request_text']
				text = text.split()

				if classification == True:
					count += 1
					self.categoryOccurrences['upvotes'].append(post['requester_upvotes_minus_downvotes_at_retrieval'])
				
				for word in text:
					for category in self.categories.keys():
						if word in self.categories[category]:
							if classification == True:
								self.categoryOccurrences[category] += 1
							else:
								self.categoryOccurrences[category] -= 1

		return 


def main ():
	path = '/Users/robertabbott/Desktop/CS/kaggle/pizza/pizza_request_dataset.json'
	t = train(path)
	t.getDataset ()
	t.getCategories ('categories.txt')
	t.mapDataByCategory ()

main()