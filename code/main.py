from train import train
from classify import classify
import random

def getProbability (trainData, c):
	correctCount = 0
	incorrectCount = 0 
	k = []
	for i in range (1000):
		h = random.random()
		l= random.random()
		randHigh = max(l, h)
		randLow = min(l, h)
	# print randHigh, randLow

		for post in trainData.dataset:
			probability = 0
			count = 1

			for word in post['request_text'].split():
				if c.probabilityForWord (word) < 0.4 or c.probabilityForWord (word) > 0.7:
					count += 1
					probability += c.probabilityForWord (word)

			probability /= count

			if probability > randHigh:
				if False == post['requester_received_pizza']:
					correctCount += 1
				else:
					incorrectCount += 1

			elif probability < randLow:
				if True == post['requester_received_pizza']:
					correctCount += 1
				else:
					incorrectCount += 1

			k.append ([correctCount, randHigh, randLow])

	m = 100000
	mi = 0
	for i in range(len(k)):
		if k[i[0]] < m:
			m = k[i[0]]
			mi = i

	return l[mi]
	return randHigh, randLow, correctCount, incorrectCount


def main ():
	trainPath = '/Users/robertabbott/Desktop/CS/kaggle/pizza/pizza_request_dataset.json'
	testPath = '/Users/robertabbott/Desktop/CS/kaggle/pizza/pizza_request_dataset.json'
	# testPath = '/Users/robertabbott/Desktop/CS/kaggle/pizza/test.json'

	trainData = train (trainPath)
	trainData.mapData ()
	c = classify (trainData, testPath)

	print getProbability (trainData, c)

	# print train.dataset
	# print train.wordCount
	# print train.wordOccurrenceCount
	# print trainData.trueDocCount
	# print trainData.falseDocCount


main ()

