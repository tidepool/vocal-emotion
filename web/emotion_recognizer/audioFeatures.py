from pymir import AudioFile
import numpy as np
from svm_interface import NormalizeVector

version = 2

def FeatureVectorForAudioFile(filename):
	# jank random parameter version
	if version == 1:
		featureVector = []
		wavData = AudioFile.open(filename)
		spectrumData = wavData.spectrum()

		featureVector.append(wavData.rms())
		featureVector.append(spectrumData.mean())
		featureVector.append(wavData.zcr())
		featureVector.append(spectrumData.centroid())
		featureVector.append(spectrumData.variance())
		featureVector.append(spectrumData.rolloff())

		mfcc = spectrumData.mfcc2()
		for i in range(12):
			featureVector.append(mfcc[i])
		
		featureVector = NormalizeVector(featureVector)
		return featureVector

	# more thought out - frame-by-frame and mean/std of rms,pitch,mfcc
	if version == 2:
		featureVector = []

	wavData = AudioFile.open(filename)
	windowFunction = np.hamming
	fixedFrames = wavData.frames(1024, windowFunction)

	rms = []
	mfcc = []
	spectralMean = []
	# spectralCentroid = []
	# spectralRolloff = []
	# spectralSkewness = []
	# spectralSpread = []
	# spectralVariance = []


	for frame in fixedFrames:
		try:
			spectrum = frame.spectrum()
			rms.append(frame.rms())
			mfcc.append(spectrum.mfcc2())
			spectralMean.append(spectrum.mean())
		except:
			pass
		# spectralCentroid.append(spectrum.centroid())
		# spectralRolloff.append(spectrum.rolloff())
		# spectralSkewness.append(spectrum.skewnness())
		# spectralSpread.append(spectrum.spread())
		# spectralVariance.append(spectrum.variance())
		# # featureVector.append(wavData.rms())
		# featureVector.append(wavSpectrum.mean())
		# featureVector.append(wavData.zcr())
		# featureVector.append(wavSpectrum.centroid())
		# featureVector.append(wavSpectrum.variance())
		# featureVector.append(wavSpectrum.rolloff())


	#normalize vectors
	rms = NormalizeVector(rms)
	for mfccInTime in mfcc:
		mfccInTime = NormalizeVector(mfccInTime)
	spectralMean = NormalizeVector(spectralMean)

	# calculate mean of all features
	rmsMean = np.mean(rms, axis = 0)
	mfccMean = np.mean(mfcc, axis = 0)
	spectralMeanMean = np.mean(spectralMean, axis = 0)

	# calculate std of all features
	rmsStd = np.std(rms, axis = 0)
	mfccStd = np.std(mfcc, axis = 0)
	spectralMeanStd = np.std(spectralMean, axis = 0)

	# add to feature vector
	featureVector.append(rmsMean)
	featureVector.append(rmsStd)
	featureVector.append(spectralMeanMean)
	featureVector.append(spectralMeanStd)

	for i in range(12):
		featureVector.append(mfccMean[i])
		featureVector.append(mfccStd[i])

	return featureVector