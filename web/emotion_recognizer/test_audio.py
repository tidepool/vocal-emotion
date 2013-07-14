from audioFeatures import *
from os import listdir
from svmutil import *

def FeatureVectorForAllFiles(directory):
	classification = []
	inputData = []
	labelHash = {
	'W': 0,
	'L': 1,
	'E': 2,
	'A': 3,
	'F': 4,
	'T': 5,
	'N': 6,
	}
	files = listdir(directory)
	for file in files:
		print 'processing -' + file
		if file[-4:-1] == ".wa":
			filename = directory + '/' + file
			featureVector = FeatureVectorForAudioFile(filename)
			label = labelHash[filename[-6]]
			classification.append(label)
			inputData.append(featureVector)
	featureData = {'classification': classification,
					'data': inputData,
					}
	return featureData

def PerformSVM():
	trainingFile = 'male' + str(version) + '.txt'
	testFile = 'male' + str(version) + '.txt'
	featureData = LoadTrainingDataFromFile(trainingFile)
	# prune data for svm tuning
	classification = []
	data = []
	emotionsToClassify = [0, 1, 2, 3, 4, 5, 6]
	for i in range(len(featureData['data'])):
		label = featureData['classification'][i]
		# if True:
		if label in emotionsToClassify:
			data.append(featureData['data'][i])
			classification.append(featureData['classification'][i])
	m = CreateSVMModel(classification, data)

	testData = FeatureVectorForAudioFile('test.wav')
	print PredictSVM(m, testData)
	return
	# compare against test database
	testData = LoadTrainingDataFromFile(testFile)

# #	stats on training data	
	success = 0
	failure = 0
	for i in range(len(testData['data'])):
		prediction = PredictSVM(m, testData['data'][i])
		# if True:
		if testData['classification'][i] in emotionsToClassify:
			if testData['classification'][i] == prediction:
				success += 1
			else:
				failure += 1
	print success
	print failure
	print 100.0 * (success)/(success+failure)



# FeatureVectorForAllFiles()
# PerformSVM()
