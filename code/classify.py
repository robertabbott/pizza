from words import words
from train import train
from parseData import parseData
from collections import defaultdict

class classify:
	MIN_WORD_COUNT = 10
	RARE_WORD_PROB = 0.3
	EXCLUSIVE_WORD_PROB = 5

	
	def __init__ (self, trainingData):
		self.trainingData = trainingData

	def probabilityForMetaData (self, post):
		# classification = post['requester_received_pizza']
		prob = 0

		# for each feature calculate probability based on training data
		# weight different features more heavily?
		for feature in self.trainingData.featureList:
			val = self.trainingData.getFeatureVal(post, feature)
			feature_count_True = self.trainingData.metaDataFeatures[True][feature][val]
			feature_count_False = self.trainingData.metaDataFeatures[False][feature][val]

			if feature_count_False == 0:
				prob += 1 - self.EXCLUSIVE_WORD_PROB
			elif feature_count_True == 0:
				prob += self.EXCLUSIVE_WORD_PROB
			else:
				pT = float(feature_count_True)
				pF = float(feature_count_False)

				prob += (pF / (pF + pT)) 	

		return prob/(len(self.trainingData.featureList))

	def probabilityForWord(self, word):
		# total_word_count = self.trainingData.wordCountTotal['False'] + self.trainingData.wordCountTotal['True'] 

		word_count_doctype2 = self.trainingData.wordOccurrenceCount['False'][word]
		word_count_doctype1 = self.trainingData.wordOccurrenceCount['True'][word]
		total_word_conut = word_count_doctype2 + word_count_doctype1
		
		if word_count_doctype1 + word_count_doctype2 < self.MIN_WORD_COUNT:
			return self.RARE_WORD_PROB

		if word_count_doctype1 == 0:
			return 1 - self.EXCLUSIVE_WORD_PROB
		elif word_count_doctype2 == 0:
			return self.EXCLUSIVE_WORD_PROB
		else:
			# low probability indicates word is likely to occur in true docs
			p_ws = float(word_count_doctype2) / float(self.trainingData.wordCountTotal['False'])
			p_wh = float(word_count_doctype1) / float(self.trainingData.wordCountTotal['True'])

			# print p_ws / (p_ws + p_wh), word
			return p_ws / (p_ws + p_wh)

	def getProbability (self, testData):
		f = open ('data.csv', 'w')
		f.write ('request_id,requester_received_pizza' + '\n')

		METADATA_WEIGHT = 10
		THRESHOLD_PROBABILITY = 0.3

		for post in testData.dataset:
			output = 0
			probability = 0
			count = 1

			# metaDataProbability
			metaDataProb = self.probabilityForMetaData(post)
			# print metaDataProb, post['requester_received_pizza']
			if metaDataProb < THRESHOLD_PROBABILITY or metaDataProb > 1- THRESHOLD_PROBABILITY:
				count += METADATA_WEIGHT
				probability += metaDataProb*METADATA_WEIGHT

			# textProbability
			for word in post['request_text_edit_aware'].split():
				if self.probabilityForWord (word) < THRESHOLD_PROBABILITY or self.probabilityForWord (word) > 0.95 - THRESHOLD_PROBABILITY:
					count += 1
					probability += self.probabilityForWord (word)

			for word in post['request_title'].split():
				if self.probabilityForWord (word) < THRESHOLD_PROBABILITY or self.probabilityForWord (word) > 0.95 - THRESHOLD_PROBABILITY:
					count += 1
					probability += self.probabilityForWord (word)

			probability /= count

			# print probability, post['requester_received_pizza']

			if probability == 0:
				# True
				output = 1

			elif probability > THRESHOLD_PROBABILITY:
				# False
				output = 0

			elif probability < THRESHOLD_PROBABILITY:
				# True
				output = 1
			else:
				# False
				output = 0

			f.write (post['request_id'] + ',' + str(output) + '\n')

		# print k
		f.close()
		return 

	def p_from_list(self, l):
		p_product         = reduce(lambda x,y: x*y, l)
		p_inverse_product = reduce(lambda x,y: x*y, map(lambda x: 1-x, l))

		return p_product / (p_product + p_inverse_product)

	def execute(self):
		pl = []

		d = db.get_doctype_counts()
		self.doctype1_count = d.get(self.doctype1)
		self.doctype2_count = d.get(self.doctype2)

		self.doctype1_word_count = db.get_words_count(self.doctype1)
		self.doctype2_word_count = db.get_words_count(self.doctype2)

		for word in self.words:
			p = self.p_for_word(db, word)
			pl.append(p)

		result = self.p_from_list(pl)

		return result































