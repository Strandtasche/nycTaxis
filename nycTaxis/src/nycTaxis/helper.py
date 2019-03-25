import sys
import glob
import pandas as pd
import numpy as np


def loadFile(path):
	# load a single csv file
	print("loading file {}...".format(path))
	dataFrameTaxisFull = pd.read_csv(path)
	print("... done!")

	# determine duration of individual trips
	dataFrameTaxisFull['tpep_pickup_datetime'] = pd.to_datetime(dataFrameTaxisFull['tpep_pickup_datetime'])
	dataFrameTaxisFull['tpep_dropoff_datetime'] = pd.to_datetime(dataFrameTaxisFull['tpep_dropoff_datetime'])

	dataFrameTaxisFull['duration'] = dataFrameTaxisFull['tpep_dropoff_datetime'] - dataFrameTaxisFull['tpep_pickup_datetime']
	# convert datetime to int (seconds)
	dataFrameTaxisFull['duration'] = dataFrameTaxisFull['duration']/np.timedelta64(1, 's')

	return dataFrameTaxisFull

def loadFolder(path):

	print("loading all files from Folder {}...".format(path))
	fileList = sorted(glob.glob(path + '/*.csv'))

	masterDataFrame = pd.DataFrame()
	for file in fileList:
		loadedData = loadFile(file)
		reducedDataFrame = condenseData(loadedData)

		# Fehlerkorrektur mit falschen Timestamps in den Daten
		reducedDataFrame = reducedDataFrame.loc[~(reducedDataFrame == 0).all(axis=1)]

		masterDataFrame = masterDataFrame.append(reducedDataFrame)

	print("all files from Folder {} loaded.".format(path))
	return masterDataFrame


def condenseData(inputDataFrame):
	# aggregate Data and remove unnecessary information
	reducedDataFrame = inputDataFrame[['tpep_pickup_datetime', 'duration']].resample('d', on='tpep_pickup_datetime').sum()
	countSeries = inputDataFrame[['tpep_pickup_datetime', 'duration']].resample('d', on='tpep_pickup_datetime').duration.count()
	reducedDataFrame['count'] = countSeries

	# remove days with no trips at all - necessary?
	# Fehlerkorrektur mit falschen Timestamps in den Daten
	reducedDataFrame.dropna(inplace=True)
	reducedDataFrame = reducedDataFrame.loc[~(reducedDataFrame == 0).all(axis=1)]

	return reducedDataFrame


def calculateAverage(inputDataFrame):
	return inputDataFrame['duration'].sum() / inputDataFrame['count'].sum()


def saveDataFrame(inputDataFrame, saveLoc='./data.h5'):

	with pd.HDFStore(saveLoc) as store:
		store['data'] = inputDataFrame


def loadDataFrame(inputDataFrame, saveLoc='./data.h5'):
	try:
		with pd.HDFStore(saveLoc) as store:
			return store['data']

	except Exception as e:
		print("Error while loading from stored data: {}".format(e))
		sys.exit(1)
