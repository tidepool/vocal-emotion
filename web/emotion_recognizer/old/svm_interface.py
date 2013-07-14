import pickle
from svmutil import *
import numpy as np

# featureData is structured as a dictionary
# featureData = {'classification': [],
#				 'data': [],
#				}

def SaveTrainingDataToFile(filename, featureData):
	f = open(filename,'wb+')
	pickle.dump(featureData, f)

def LoadTrainingDataFromFile(filename):
	f = open(filename,'r+')
	featureData = pickle.load(f)
	return featureData

def CreateSVMModel(featureData):
	prob = svm_problem(featureData['classification'], featureData['data'])
	param = svm_parameter()
	param.kernel_type = RBF
	param.C=50
	m = svm_train(prob, param)
	return m
	
def PredictSVM(model, data):
	svm_model.predict = lambda self, x: svm_predict([0], [x], self)[0][0]
	return model.predict(data)

def NormalizeVector(vector):
	# normalize vectors
	normalizingVector = np.max(np.abs(vector),axis=0)
	vector = np.array(vector,dtype=float)
	vector /= normalizingVector
	vector = vector.tolist()
	return vector

def PlotFeaturesAgainstEachOther():
	import matplotlib.pyplot as plt
	data = LoadTrainingDataFromFile('female.txt')
	features = data['data']
	features = np.array(NormalizeVector(features)).T
	# for i in range(len(features)):
	# 	label = data['classification'][i]
	# 	if label == 0 or label == 6 or True:
	# 		first.append(features[0])
	# 		second.append(features[1])
	# 		color.append([label/6.0,label/6.0,label/6.0])
	# print len(first)
	for i in range(17):
		for j in range(17):
			plt.scatter(features[i],features[j],c=data['classification'],s=100)
			plt.gray()
			print i, j
			plt.show()