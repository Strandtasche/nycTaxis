import pandas as pd
import numpy as np
import os
import glob

from nycTaxis.dataHandler import loadFile
from nycTaxis.dataHandler import condenseData
from nycTaxis.dataHandler import calculateAverage


def averageMonthNaive(inputDataPath):
	# Basic Case: load csv of a month and calculate average
	data = loadFile(inputDataPath)
	averageDuration = data['duration'].mean()
	return averageDuration




def main():
	dirName = os.path.dirname(__file__)
	# dataFolderPath = os.path.join(dirName, '../../data/')
	dataFolderPath = '/home/tobi/Projects/BlueYonder/data'

	fileList = sorted(glob.glob(dataFolderPath + '/*.csv'))

	masterDataFrame = pd.DataFrame()
	for file in fileList:
		loadedData = loadFile(file)
		reducedDataFrame = condenseData(loadedData)


		masterDataFrame = masterDataFrame.append(reducedDataFrame)


	print("files loaded")
	rollingAverage = masterDataFrame['duration'].rolling(window=45).sum() / masterDataFrame['count'].rolling(window=45).sum()
	print(rollingAverage)

	# print("done loading: len(durationList) = {}".format(len(durationList)))

if __name__ == '__main__':
	main()
