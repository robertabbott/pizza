import json
import csv
import codecs
import datetime

from words import words
from parseData import parseData
from collections import defaultdict


class train:

	def __init__ (self, path):
		self.dataset = parseData.readDataset (path)
		self.wordCount = defaultdict (int)
		self.wordOccurrenceCount = {'True':defaultdict (int), 'False':defaultdict (int)}
		self.wordCountTotal = {'True':0, 'False':0}
		self.docCount = 0
		self.trueCount = 0
		self.metaDataFeatures = {True:defaultdict(), False:defaultdict()}
		self.featureList = ['upvotes', 'voteRatio', 'unix_timestamp_of_request_utc', 'requester_user_flair']

	def addDataSet (self, path):
		self.dataset = parseData.readDataset (path)

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


	def mapFeatures (self, post):
		for feature in self.featureList:
			if post['requester_received_pizza'] == True:
				# classification, feature, bucket
				self.metaDataFeatures[True][feature][self.getFeatureVal(post, feature)] += 1

			else:
				self.metaDataFeatures[False][feature][self.getFeatureVal(post, feature)] += 1		

	def getFeatureVal (self, post, feature):
		if feature == 'upvotes':
			upvotes = int(post['requester_upvotes_minus_downvotes_at_retrieval'])
			upvotes -= upvotes % 100
			return upvotes/100
		if feature == 'voteRatio':
			if post['number_of_downvotes_of_request_at_retrieval'] != 0:
				voteRatio = int(post['number_of_upvotes_of_request_at_retrieval'] / post['number_of_downvotes_of_request_at_retrieval'])
			else:
				voteRatio = int(post['number_of_upvotes_of_request_at_retrieval'])

			return voteRatio

		if feature == 'unix_timestamp_of_request_utc':
			hour = datetime.datetime.fromtimestamp(int(post['unix_timestamp_of_request_utc'])).strftime('%Y-%m-%d %H:%M:%S')
			hour = hour.split()[1]
			hour = int(hour.split(':')[0])

			return hour

		if feature == 'requester_user_flair':
			return post['requester_user_flair']


	def mapMetaData (self, post):
		# non-parametric distribution of numerical metadata
		self.mapFeatures (post)

	def setFeatures (self):
		for feature in self.featureList:
			self.metaDataFeatures[True][feature] = defaultdict(int)
			self.metaDataFeatures[False][feature] = defaultdict(int)

	def mapData (self):
		self.setFeatures ()
		categories = self.getCategories ('/Users/robertabbott/Desktop/CS/projects/kaggle/pizza/code/wordLists/')
		if self.dataset == None:
			return
		else:
			count = 0
			tWordList = []
			fWordList = []
			trueCount = 0
			docCount = 0
			for post in self.dataset:
				docCount += 1
				self.mapMetaData (post)
				classification = post['requester_received_pizza']

				if classification == True:
					trueCount = 0
					# self.docCount['True'] += 1
					tWordList += self.words.textToList(post['request_text'])
				else:
					# self.docCount['False'] += 1
					fWordList += self.words.textToList(post['request_text'])

				

			textMapT = self.words.listToDict (tWordList)
			textMapF = self.words.listToDict (fWordList)


			for word in textMapT.keys():
				self.wordCountTotal['True'] += textMapT[word]
				if categories['stopwords'][word] != 1:
					self.wordCount[word] += textMapT[word]
					self.wordOccurrenceCount['True'][word] += textMapT[word]

			for word in textMapF.keys():
				self.wordCountTotal['False'] += textMapF[word]
				if categories['stopwords'][word] != 1:
					self.wordCount[word] -= textMapF[word]
					self.wordOccurrenceCount['False'][word] += textMapF[word]


			self.docCount = docCount
			self.trueCount = trueCount
			# print self.wordCount
			# print self.wordOccurrenceCount
			# print self.wordCountTotal['False']
			# print self.wordCountTotal['True']
		return 





def main ():
	path = '/Users/robertabbott/Desktop/CS/kaggle/pizza/pizza_request_dataset.json'
	t = train(path)
	t.mapData ()
	# print t.metaDataFeatures[True]['upvotes'].keys()
	# print t.metaDataFeatures[False]['upvotes'].keys()
	# print t.metaDataFeatures[True]['voteRatio'].keys()
	# print t.metaDataFeatures[False]['voteRatio'].keys()
	# t.addDataSet ('/Users/robertabbott/Desktop/CS/kaggle/pizza/train.json')
	# t.mapData ()

# main()








