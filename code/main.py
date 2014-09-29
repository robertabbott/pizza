from train import train
from classify import classify
import random
import time

def main ():
	x = time.clock ()
	# trainPath = '/Users/robertabbott/Desktop/CS/projects/kaggle/pizza/pizza_request_dataset.json'
	testPath = '/Users/robertabbott/Desktop/CS/projects/kaggle/pizza/pizza_request_dataset.json'
	# testPath = '/Users/robertabbott/Desktop/CS/kaggle/pizza/test.json'

	testData = train (testPath)
	trainData = train ('/Users/robertabbott/Desktop/CS/projects/kaggle/pizza/train.json')
	trainData.mapData ()
	# trainData.addDataSet (trainPath)
	c = classify (trainData, testPath)

	# y = getProbability (testData, c)
	y = c.getProbability (testData)
	print y[0:2]
	print 'positives: ' + str(y[2]), 'negatives: ' + str(y[3])
	print 'false positives: ' + str(y[4]), 'false negatives: ' + str(y[5])
	print 'recall = ' + str(float(y[2])/float(y[2]+y[4]))
	print 'precision = ' + str(float(y[2])/float(y[2]+y[5]))
	print 'accuracy = ' + str(float(y[0]) / (float(y[0])+float(y[1])))
	# print time.clock() - x
	# print train.dataset
	# print train.wordCount
	# print train.wordOccurrenceCount
	# print trainData.trueDocCount
	# print trainData.falseDocCount


main ()

