import pandas as pd
import numpy as np
import os
import sys
import glob
import datetime

from nycTaxis.dataHandler import loadFileRaw
from nycTaxis.dataHandler import condenseData
from nycTaxis.dataHandler import calculateRollingAverage



def averageMonthNaive(inputDataPath):
	"""Basic Case: load csv of a month and calculate average duration"""
	data = loadFileRaw(inputDataPath)
	averageDuration = data['duration'].mean()
	return averageDuration

def rollingAverageDate(inputDataFrame, dateString):
	"""receives a dataframe and a date and returns the rolling average on that date"""
	assert 'rollingAvg' in inputDataFrame.columns

	_validate(dateString)
	if dateString not in inputDataFrame.index:
		raise ValueError("given date is not part of dataset")
	else:
		return inputDataFrame['rollingAvg'].loc[dateString].values[0]

def rollingAverageTotal(inputDataFrame):
	"""returns the whole rolling average of a dataframe"""
	assert 'rollingAvg' in inputDataFrame.columns
	return inputDataFrame['rollingAvg']

def _validate(date_text):
	try:
		datetime.datetime.strptime(date_text, '%Y-%m-%d')
	except ValueError:
		raise ValueError("Incorrect Date Format, should be YYYY-MM-DD")


def main():
	dirName = os.path.dirname(__file__)
	# dataFolderPath = os.path.join(dirName, '../../data/')
	dataFolderPath = '/home/tobi/Projects/BlueYonder/data'

	fileList = sorted(glob.glob(dataFolderPath + '/*.csv'))

	masterDataFrame = pd.DataFrame()
	for file in fileList:
		loadedData = loadFileRaw(file)
		reducedDataFrame = condenseData(loadedData)


		masterDataFrame = masterDataFrame.append(reducedDataFrame)


	print("files loaded")
	rollingAverage = masterDataFrame['duration'].rolling(window=45).sum() / masterDataFrame['count'].rolling(window=45).sum()
	print(rollingAverage)

	# print("done loading: len(durationList) = {}".format(len(durationList)))

if __name__ == '__main__':
	main()
