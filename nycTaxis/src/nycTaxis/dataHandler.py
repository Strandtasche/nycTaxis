import sys
import glob
import pandas as pd
import numpy as np
import os


def loadFileRaw(path):
	"""load a single csv file"""

	assert os.path.exists(path)
	print("loading file {}...".format(path))
	dataFrameTaxisFull = pd.read_csv(path)
	print("... done!")

	# determine duration of individual trips
	dataFrameTaxisFull['tpep_pickup_datetime'] = pd.to_datetime(dataFrameTaxisFull['tpep_pickup_datetime'])
	dataFrameTaxisFull['tpep_dropoff_datetime'] = pd.to_datetime(dataFrameTaxisFull['tpep_dropoff_datetime'])

	#remove wrongly dated data points
	dataFrameTaxisFull = filterDataFrame(dataFrameTaxisFull, os.path.basename(path))

	dataFrameTaxisFull['duration'] = dataFrameTaxisFull['tpep_dropoff_datetime'] - dataFrameTaxisFull['tpep_pickup_datetime']
	# convert datetime to int (seconds)
	dataFrameTaxisFull['duration'] = dataFrameTaxisFull['duration']/np.timedelta64(1, 's')

	return dataFrameTaxisFull


def filterDataFrame(inputDataFrame, name):
	"""removes datapoints outside of designated timeframe"""

	assert 'tpep_pickup_datetime' in inputDataFrame.columns
	assert len(name) == 27 and '.csv' in name
	year = int(name[16:20])
	month = int(name[21:23])

	mask = (inputDataFrame['tpep_pickup_datetime'].dt.month == month) & (inputDataFrame['tpep_pickup_datetime'].dt.year == year)
	filteredDataFrame = inputDataFrame.loc[mask]

	return filteredDataFrame


def loadFile(path):
	""" loads and condenses a single csv file"""

	assert os.path.exists(path)
	masterDataFrame = loadFileRaw(path)
	reducedDataFrame = condenseData(masterDataFrame)

	return reducedDataFrame


def loadFolder(path):
	"""load and condense all csv files in a folder"""

	assert os.path.exists(path)
	print("loading all files from Folder {}...".format(path))
	# list of all csv files in Folder
	fileList = sorted(glob.glob(path + '/*.csv'))

	masterDataFrame = pd.DataFrame()
	for file in fileList:
		loadedData = loadFileRaw(file)
		reducedDataFrame = condenseData(loadedData)

		masterDataFrame = masterDataFrame.append(reducedDataFrame)

	print("all files from Folder {} loaded.".format(path))
	return masterDataFrame


def condenseData(inputDataFrame):
	"""aggregate Data and remove unnecessary information"""
	assert 'tpep_pickup_datetime' in inputDataFrame.columns
	assert 'duration' in inputDataFrame.columns
	reducedDataFrame = inputDataFrame[['tpep_pickup_datetime', 'duration']].resample('d', on='tpep_pickup_datetime').sum()
	countSeries = inputDataFrame[['tpep_pickup_datetime', 'duration']].resample('d', on='tpep_pickup_datetime').duration.count()
	reducedDataFrame['count'] = countSeries

	# reducedDataFrame.dropna(inplace=True)
	# reducedDataFrame = reducedDataFrame.loc[~(reducedDataFrame == 0).all(axis=1)]

	return reducedDataFrame


def calculateRollingAverage(inputDataFrame):
	"""calculates the rolling average an a condensed dataframe"""

	assert 'duration' in inputDataFrame.columns
	assert 'count' in inputDataFrame.columns
	# win_type can change the kind of rolling average we are getting.
	inputDataFrame['rollingAvg'] = inputDataFrame['duration'].rolling(window=45).sum() / inputDataFrame['count'].rolling(window=45).sum()

	# replace NaN Values with 0? except at the start?
	# inputDataFrame['rollingAvg'].fillna(0.0, inplace=True)

	return inputDataFrame, inputDataFrame['rollingAvg']


def appendDataFrame(inputDataFrame, path):
	"""take a given dataframe and append another, extracted from a file"""

	assert 'duration' in inputDataFrame.columns
	assert 'count' in inputDataFrame.columns

	appendingDataFrame = pd.DataFrame()
	if os.path.isdir(path):
		appendingDataFrame = loadFolder(path)
	elif os.path.isfile(path):
		appendingDataFrame = loadFile(path)
	assert appendingDataFrame.columns.isin(inputDataFrame.columns).all()

	if appendingDataFrame.index.isin(inputDataFrame.index).any():
		print("Warning, you're adding already existing indices to the dataFrame")

	returnDataFrame = inputDataFrame.append(appendingDataFrame, sort=False)
	returnDataFrame.sort_index(inplace=True)
	returnDataFrame, _ = calculateRollingAverage(returnDataFrame)

	return returnDataFrame


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
