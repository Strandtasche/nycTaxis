import sys
import glob
import pandas as pd
import numpy as np


def loadFile(path):
	"""load a single csv file"""
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
	"""load all csv files in a folder"""
	print("loading all files from Folder {}...".format(path))
	# list of all csv files in Folder
	fileList = sorted(glob.glob(path + '/*.csv'))

	masterDataFrame = pd.DataFrame()
	for file in fileList:
		loadedData = loadFile(file)
		reducedDataFrame = condenseData(loadedData)

		masterDataFrame = masterDataFrame.append(reducedDataFrame)

	print("all files from Folder {} loaded.".format(path))
	return masterDataFrame


def condenseData(inputDataFrame):
	"""aggregate Data and remove unnecessary information"""
	reducedDataFrame = inputDataFrame[['tpep_pickup_datetime', 'duration']].resample('d', on='tpep_pickup_datetime').sum()
	countSeries = inputDataFrame[['tpep_pickup_datetime', 'duration']].resample('d', on='tpep_pickup_datetime').duration.count()
	reducedDataFrame['count'] = countSeries

	# remove days with no trips at all - necessary?
	# Fehlerkorrektur mit falschen Timestamps in den Daten
	reducedDataFrame.dropna(inplace=True)
	reducedDataFrame = reducedDataFrame.loc[~(reducedDataFrame == 0).all(axis=1)]

	return reducedDataFrame


def calculateRollingAverage(inputDataFrame):

	# win_type can change the kind of rolling average we are getting.
	inputDataFrame['rollingAvg'] = inputDataFrame['duration'].rolling(window=45).sum() / inputDataFrame['count'].rolling(window=45).sum()

	# replace NaN Values with 0? except at the front? TODO: Decision
	# inputDataFrame['rollingAvg'].fillna(0.0, inplace=True)

	return inputDataFrame, inputDataFrame['rollingAvg']


def saveDataFrame(inputDataFrame, saveLoc='./data.h5'):
	"""take a given dataframe and save it as a h5 file"""
	print("Saving Dataframe to {}.".format(saveLoc))
	with pd.HDFStore(saveLoc) as store:
		store['data'] = inputDataFrame


def loadDataFrame(saveLoc='./data.h5'):
	"""loads and returns a dataframe from the given location"""
	print("Loading Dataframe from {}".format(saveLoc))
	try:
		with pd.HDFStore(saveLoc) as store:
			return store['data']

	except Exception as e:
		print("Error while loading from stored data: {}".format(e))
		sys.exit(1)
