from faceFeatures import *
from os import listdir
from svm_interface import *

emotionToNumber = {
	'angry': 0,
	'happy': 1,
	'scared': 2,
	'neutral': 3,
	'sad': 4,
	'bored': 5,
	'disgusted': 6,
	'surprised': 7,	
}

numberToEmotion = {v:k for k, v in emotionToNumber.items()}

def FeatureVectorForAllFiles(directory):
	classification = []
	inputData = []
	files = listdir(directory)
	for file in files:
		print 'processing -' + file
		if file[-4:-1] == ".jp":
			filename = directory + '/' + file
			featureVector = FacialFeaturesForPhoto(filename)
			label = emotionToNumber[filename.split('/')[-1].split('-')[0]]
			classification.append(label)
			inputData.append(featureVector)
	featureData = {'classification': classification,
					'data': inputData,
					}
	return featureData


def PerformSVM():
	featureData = LoadTrainingDataFromFile('mayank.txt')
	normalizingVector = NormalizeVector(featureData['data'])
	# prune data for svm tuning
	classification = []
	data = []
	emotionsToClassify = [0, 1, 2, 3, 4, 5, 6, 7]

	for i in range(len(featureData['data'])):
		label = featureData['classification'][i]
		# if True:
		if label in emotionsToClassify:
			data.append(featureData['data'][i])
			classification.append(featureData['classification'][i])
	features = {
				'classification': classification,
				'data': data,
				}
	m = CreateSVMModel(features)

	testData = FacialFeaturesForPhoto('test.jpg')
	# testData['data'] /= normalizingVector
	print numberToEmotion[PredictSVM(m,testData)]
	return
	success = 0
	failure = 0
	testData = LoadTrainingDataFromFile('faces.txt')
	for i in range(len(testData['data'])):
		label = testData['classification'][i]
		if label in emotionsToClassify:
			print 'initial'
			if numberToEmotion[PredictSVM(m,testData['data'][i])] == numberToEmotion[testData['classification'][i]]:
				success += 1
			else:
				failure += 1
	print success, failure, 1.0 * success / (success+failure)

# features = FeatureVectorForAllFiles('photos')
# SaveTrainingDataToFile('mayank.txt', features)
# featureData = LoadTrainingDataFromFile('faces.txt')
PerformSVM()
# print featureData