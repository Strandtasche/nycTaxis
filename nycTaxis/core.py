#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pandas as pd
import os
import glob


def loadData(path):
	# load a single csv file
	dataFrameTaxisFull = pd.read_csv(path)

	# determine duration of individual trips
	dataFrameTaxisFull['tpep_pickup_datetime'] = pd.to_datetime(dataFrameTaxisFull['tpep_pickup_datetime'])
	dataFrameTaxisFull['tpep_dropoff_datetime'] = pd.to_datetime(dataFrameTaxisFull['tpep_dropoff_datetime'])

	dataFrameDuration = dataFrameTaxisFull['tpep_dropoff_datetime'] - dataFrameTaxisFull['tpep_pickup_datetime']

	return dataFrameDuration


def main():
	dirName = os.path.dirname(__file__)
	dataFolderPath = os.path.join(dirName, '../data/')

	fileList = sorted(glob.glob(dataFolderPath + '/*.csv'))

	durationList = []
	for file in fileList:
		durationList.append(loadData(file))

	print("done loading: len(durationList) = {}".format(len(durationList)))

if __name__ == '__main__':
    main()
