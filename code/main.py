from train import train
from classify import classify
import random

def getProbability (trainData, c):
	correctCount = 0
	incorrectCount = 0 
	# k = []
	# for i in range (1000):
	# 	h = random.random()
	# 	l= random.random()
	# 	randHigh = max(l, h)
	# 	randLow = min(l, h)
	# print randHigh, randLow

	randHigh = 0.3
	randLow = randHigh

	for post in trainData.dataset:
		probability = 0
		count = 1

		# metaDataProbability
		metaDataProb = c.probabilityForMetaData(post)
		# print metaDataProb, post['requester_received_pizza']
		if metaDataProb < 0.3 or metaDataProb > 0.7:
			count += 10
			probability += metaDataProb*10

		# textProbability
		for word in post['request_text'].split():
			if c.probabilityForWord (word) < 0.3 or c.probabilityForWord (word) > 0.65:
				count += 1
				probability += c.probabilityForWord (word)

		probability /= count

		# print probability, post['requester_received_pizza']

		if probability == 0:
			if False == post['requester_received_pizza']:
				correctCount += 1
			else:
				incorrectCount += 1

		elif probability > randHigh:
			if False == post['requester_received_pizza']:
				correctCount += 1
			else:
				incorrectCount += 1

		elif probability < randLow:
			if True == post['requester_received_pizza']:
				correctCount += 1
			else:
				incorrectCount += 1

		# k.append ([correctCount, randHigh, randLow])

	# m = 100000
	# mi = 0
	# for i in range(len(k)):
	# 	if k[i[0]] < m:
	# 		m = k[i[0]]
	# 		mi = i

	# return l[mi]
	return correctCount, incorrectCount


def main ():
	trainPath = '/Users/robertabbott/Desktop/CS/kaggle/pizza/pizza_request_dataset.json'
	testPath = '/Users/robertabbott/Desktop/CS/kaggle/pizza/pizza_request_dataset.json'
	# testPath = '/Users/robertabbott/Desktop/CS/kaggle/pizza/test.json'

	testData = train (testPath)
	trainData = train ('/Users/robertabbott/Desktop/CS/kaggle/pizza/train.json')
	trainData.mapData ()
	# trainData.addDataSet (trainPath)
	c = classify (trainData, testPath)

	print getProbability (testData, c)

	# print train.dataset
	# print train.wordCount
	# print train.wordOccurrenceCount
	# print trainData.trueDocCount
	# print trainData.falseDocCount


main ()

