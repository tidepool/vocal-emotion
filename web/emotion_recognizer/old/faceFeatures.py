import logging
from betaface_api import BetaFaceAPI
import xml.etree.ElementTree as ET

def FacialFeaturesForPhoto(filename):
	facialFeatures = {}

	featureToCrypticCode = {
	'EYE_L': 512,
	'EYE_LCI': 1536,
	'EYE_LCO': 1024,
	'EYE_R': 768,
	'EYE_RCI': 1792,
	'EYE_RCO': 1280,
	'MOUTH_LC': 2048,
	'MOUTH_RC': 2304,

	'PRO_CHEEKBONE_L': 5570560,
	'PRO_CHEEKBONE_R': 5636096,

	'PRO_CHIN_B': 458752,
	'PRO_CHIN_EARCONN_L': 65536,
	'PRO_CHIN_EARCONN_R': 851968,
	'PRO_CHIN_P1_L': 131072,
	'PRO_CHIN_P1_R': 786432,
	'PRO_CHIN_P2_L': 196608,
	'PRO_CHIN_P2_R': 720896,
	'PRO_CHIN_P3_L': 262144,
	'PRO_CHIN_P3_R': 655360,
	'PRO_CHIN_P4_L': 327680,
	'PRO_CHIN_P4_R': 589824,
	'PRO_CHIN_P5_L': 393216,
	'PRO_CHIN_P5_R': 524288,

	'PRO_EYE_B_L': 2949120,
	'PRO_EYE_B_R': 2162688,
	'PRO_EYE_BI_L': 2883584,
	'PRO_EYE_BI_R': 2228224,
	'PRO_EYE_BO_L': 3014656,
	'PRO_EYE_BO_R': 2097152,
	'PRO_EYE_I_L': 2818048,
	'PRO_EYE_I_R': 2293760,
	'PRO_EYE_IRIS_L': 5439488,
	'PRO_EYE_IRIS_R': 5373952,
	'PRO_EYE_O_L': 2555904,
	'PRO_EYE_O_R': 2031616,
	'PRO_EYE_T_L': 2686976,
	'PRO_EYE_T_R': 2424832,
	'PRO_EYE_TI_L': 2752512,
	'PRO_EYE_TI_R': 2359296,
	'PRO_EYE_TO_L': 2621440,
	'PRO_EYE_TO_R': 2490368,

	'PRO_EYEBROW_B_L': 3997696,
	'PRO_EYEBROW_B_R': 3473408,
	'PRO_EYEBROW_BI_L': 4063232,
	'PRO_EYEBROW_BI_R': 3538944,
	'PRO_EYEBROW_BO_L': 3932160,
	'PRO_EYEBROW_BO_R': 3407872,
	'PRO_EYEBROW_I_L': 3604480,
	'PRO_EYEBROW_I_R': 3080192,
	'PRO_EYEBROW_O_L': 3866624,
	'PRO_EYEBROW_O_R': 3342336,
	'PRO_EYEBROW_T_L': 3735552,
	'PRO_EYEBROW_T_R': 3211264,
	'PRO_EYEBROW_TI_L': 3670016,
	'PRO_EYEBROW_TI_R': 3145728,
	'PRO_EYEBROW_TO_L': 3801088,
	'PRO_EYEBROW_TO_R': 3276800,

	'PRO_FOREHEAD_L': 1638400,
	'PRO_FOREHEAD_M': 1441792,
	'PRO_FOREHEAD_P1': 1572864,
	'PRO_FOREHEAD_P2': 1507328,
	'PRO_FOREHEAD_P3': 1376256,
	'PRO_FOREHEAD_P4': 1310720,
	'PRO_FOREHEAD_R': 1245184,

	'PRO_MOUTH_B': 4521984,
	'PRO_MOUTH_BL': 4587520,
	'PRO_MOUTH_BR': 4456448,
	'PRO_MOUTH_L': 4128768,
	'PRO_MOUTH_R': 4390912,
	'PRO_MOUTH_T': 4259840,
	'PRO_MOUTH_TL': 4194304,
	'PRO_MOUTH_TR': 4325376,

	'PRO_NOSE_B': 4980736,
	'PRO_NOSE_B_NOSTRIL_L': 4915200,
	'PRO_NOSE_B_NOSTRIL_R': 5046272,
	'PRO_NOSE_BO_NOSTRIL_L': 4849664,
	'PRO_NOSE_BO_NOSTRIL_R': 5111808,
	'PRO_NOSE_T_L': 4653056,
	'PRO_NOSE_T_R': 5308416,
	'PRO_NOSE_TI_NOSTRIL_L': 4718592,
	'PRO_NOSE_TI_NOSTRIL_R': 5242880,
	'PRO_NOSE_TIP': 5505024,
	'PRO_NOSE_TO_NOSTRIL_L': 4784128,
	'PRO_NOSE_TO_NOSTRIL_R': 5177344,

	'PRO_TEMPLE_L': 1703936,
	'PRO_TEMPLE_P1_L': 1769472,
	'PRO_TEMPLE_P1_R': 1114112,
	'PRO_TEMPLE_P2_L': 1835008,
	'PRO_TEMPLE_P2_R': 1048576,
	'PRO_TEMPLE_P3_L': 1900544,
	'PRO_TEMPLE_P3_R': 983040,
	'PRO_TEMPLE_P4_L': 1966080,
	'PRO_TEMPLE_P4_R': 917504,
	'PRO_TEMPLE_R': 1179648,
	}

	crypticCodeToFeature = {v:k for k, v in featureToCrypticCode.items()}

	def SlopeBetween(x1, y1, x2, y2):
		return (y2-y1)/(x2-x1)

	def DistBetween(x1, y1, x2, y2):
		return pow((y2-y1)*(y2-y1)/(x2-x1)*(x2-x1),0.5)

	def LEyebrowSlopeOuter(facialFeatures):
		p1 = facialFeatures['PRO_EYEBROW_O_L']
		p2 = facialFeatures['PRO_EYEBROW_T_L']
		return SlopeBetween(p1[0],p1[1],p2[0],p2[1])

	def LEyebrowSlopeInner(facialFeatures):
		p1 = facialFeatures['PRO_EYEBROW_I_L']
		p2 = facialFeatures['PRO_EYEBROW_T_L']
		return SlopeBetween(p1[0],p1[1],p2[0],p2[1])

	def REyebrowSlopeInner(facialFeatures):
		p1 = facialFeatures['PRO_EYEBROW_I_R']
		p2 = facialFeatures['PRO_EYEBROW_T_R']
		return SlopeBetween(p1[0],p1[1],p2[0],p2[1])

	def REyebrowSlopeOuter(facialFeatures):
		p1 = facialFeatures['PRO_EYEBROW_O_R']
		p2 = facialFeatures['PRO_EYEBROW_T_R']
		return SlopeBetween(p1[0],p1[1],p2[0],p2[1])

	def TSmileSlopeLeft(facialFeatures):
		p1 = facialFeatures['PRO_MOUTH_L']
		p2 = facialFeatures['PRO_MOUTH_T']
		return SlopeBetween(p1[0],p1[1],p2[0],p2[1])

	def TSmileSlopeRight(facialFeatures):
		p1 = facialFeatures['PRO_MOUTH_R']
		p2 = facialFeatures['PRO_MOUTH_T']
		return SlopeBetween(p1[0],p1[1],p2[0],p2[1])

	def BSmileSlopeLeft(facialFeatures):
		p1 = facialFeatures['PRO_MOUTH_L']
		p2 = facialFeatures['PRO_MOUTH_B']
		return SlopeBetween(p1[0],p1[1],p2[0],p2[1])

	def BSmileSlopeRight(facialFeatures):
		p1 = facialFeatures['PRO_MOUTH_R']
		p2 = facialFeatures['PRO_MOUTH_B']
		return SlopeBetween(p1[0],p1[1],p2[0],p2[1])

	def LEyeHeight(facialFeatures):
		p1 = facialFeatures['PRO_EYE_T_L']
		p2 = facialFeatures['PRO_EYE_B_L']
		return DistBetween(p1[0],p1[1],p2[0],p2[1])

	def REyeHeight(facialFeatures):
		p1 = facialFeatures['PRO_EYE_T_R']
		p2 = facialFeatures['PRO_EYE_B_R']
		return DistBetween(p1[0],p1[1],p2[0],p2[1])

	def MouthHeight(facialFeatures):
		p1 = facialFeatures['PRO_MOUTH_T']
		p2 = facialFeatures['PRO_MOUTH_B']
		return DistBetween(p1[0],p1[1],p2[0],p2[1])

	def FaceHeight(facialFeatures):
		p1 = facialFeatures['PRO_FOREHEAD_M']
		p2 = facialFeatures['PRO_CHIN_B']
		return DistBetween(p1[0],p1[1],p2[0],p2[1])

	def LEyeHeightToFaceRatio(facialFeatures):
		return LEyeHeight(facialFeatures) / FaceHeight(facialFeatures)

	def REyeHeightToFaceRatio(facialFeatures):
		return REyeHeight(facialFeatures) / FaceHeight(facialFeatures)

	def MouthHeightToFaceRatio(facialFeatures):
		return MouthHeight(facialFeatures) / FaceHeight(facialFeatures)

	logging.basicConfig(level = logging.INFO)
	client = BetaFaceAPI()

	results = client.get_image_info(filename,'features@tidepool')
	tree = ET.fromstring(results['raw_content'])
	points = tree.find('faces').find('FaceInfo').find('points').findall('PointInfo')
	for point in points:
		x = float(point.find('x').text)
		y = float(point.find('y').text)
		p = [x, y]
		facialFeatures[crypticCodeToFeature[int(point.find('type').text)]] = p

	featureVector = []
	featureVector.append(LEyebrowSlopeOuter(facialFeatures))
	featureVector.append(LEyebrowSlopeInner(facialFeatures))
	featureVector.append(REyebrowSlopeInner(facialFeatures))
	featureVector.append(REyebrowSlopeOuter(facialFeatures))

	featureVector.append(TSmileSlopeLeft(facialFeatures))
	featureVector.append(TSmileSlopeRight(facialFeatures))
	featureVector.append(BSmileSlopeLeft(facialFeatures))
	featureVector.append(BSmileSlopeRight(facialFeatures))

	featureVector.append(LEyeHeightToFaceRatio(facialFeatures))
	featureVector.append(REyeHeightToFaceRatio(facialFeatures))
	featureVector.append(MouthHeightToFaceRatio(facialFeatures))

	return featureVector