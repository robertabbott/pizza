from train import train
from classify import classify
import random
import time

def getProbability (trainData, c):
	METADATA_WEIGHT = 10
	THRESHOLD_PROBABILITY = 0.3

	correctCount = 0
	incorrectCount = 0 

	# k = []
	# for i in range (1000):
	# 	h = random.random()
	# 	l= random.random()
	# 	THRESHOLD_PROBABILITY = max(l, h)
	# 	randLow = min(l, h)
	# print THRESHOLD_PROBABILITY, randLow

	
	randLow = THRESHOLD_PROBABILITY

	for post in trainData.dataset:
		probability = 0
		count = 1

		# metaDataProbability
		metaDataProb = c.probabilityForMetaData(post)
		# print metaDataProb, post['requester_received_pizza']
		if metaDataProb < THRESHOLD_PROBABILITY or metaDataProb > 1- THRESHOLD_PROBABILITY:
			count += METADATA_WEIGHT
			probability += metaDataProb*METADATA_WEIGHT

		# textProbability
		for word in post['request_text'].split():
			if c.probabilityForWord (word) < THRESHOLD_PROBABILITY or c.probabilityForWord (word) > 0.95 - THRESHOLD_PROBABILITY:
				count += 1
				probability += c.probabilityForWord (word)

		probability /= count

		print probability, post['requester_received_pizza']

		if probability == 0:
			if False == post['requester_received_pizza']:
				correctCount += 1
			else:
				incorrectCount += 1

		elif probability > THRESHOLD_PROBABILITY:
			if False == post['requester_received_pizza']:
				correctCount += 1
			else:
				incorrectCount += 1

		elif probability < randLow:
			if True == post['requester_received_pizza']:
				correctCount += 1
			else:
				incorrectCount += 1

	return correctCount, incorrectCount


def main ():
	x = time.clock ()
	trainPath = '/Users/robertabbott/Desktop/CS/projects/kaggle/pizza/pizza_request_dataset.json'
	testPath = '/Users/robertabbott/Desktop/CS/projects/kaggle/pizza/pizza_request_dataset.json'
	# testPath = '/Users/robertabbott/Desktop/CS/kaggle/pizza/test.json'

	testData = train (testPath)
	trainData = train ('/Users/robertabbott/Desktop/CS/projects/kaggle/pizza/train.json')
	trainData.mapData ()
	# trainData.addDataSet (trainPath)
	c = classify (trainData, testPath)

	print getProbability (testData, c)
	print time.clock() - x
	# print train.dataset
	# print train.wordCount
	# print train.wordOccurrenceCount
	# print trainData.trueDocCount
	# print trainData.falseDocCount


main ()

