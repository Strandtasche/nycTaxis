#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pandas as pd
import numpy as np
import os
import glob


def loadData(path):
	# load a single csv file
	dataFrameTaxisFull = pd.read_csv(path)

	# determine duration of individual trips
	dataFrameTaxisFull['tpep_pickup_datetime'] = pd.to_datetime(dataFrameTaxisFull['tpep_pickup_datetime'])
	dataFrameTaxisFull['tpep_dropoff_datetime'] = pd.to_datetime(dataFrameTaxisFull['tpep_dropoff_datetime'])

	dataFrameTaxisFull['duration'] = dataFrameTaxisFull['tpep_dropoff_datetime'] - dataFrameTaxisFull['tpep_pickup_datetime']
	dataFrameTaxisFull['duration'] = dataFrameTaxisFull['duration']/np.timedelta64(1, 's')

	return dataFrameTaxisFull


def averageMonthNaive(inputSeries):
	return inputSeries.mean()


def condenseData(inputDataFrame):
	# aggregate Data and remove unnecessary information
	reducedDataFrame = inputDataFrame[['tpep_pickup_datetime', 'duration']].resample('d', on='tpep_pickup_datetime').sum()
	countSeries = inputDataFrame[['tpep_pickup_datetime', 'duration']].resample('d', on='tpep_pickup_datetime').duration.count()
	reducedDataFrame['count'] = countSeries

	# remove days with no trips at all
	reducedDataFrame.dropna(inplace=True)

def main():
	dirName = os.path.dirname(__file__)
	dataFolderPath = os.path.join(dirName, '../data/')

	fileList = sorted(glob.glob(dataFolderPath + '/*.csv'))

	durationList = []
	for file in fileList:
		loadedData = loadData(file)
		





	print("done loading: len(durationList) = {}".format(len(durationList)))

if __name__ == '__main__':
	main()
