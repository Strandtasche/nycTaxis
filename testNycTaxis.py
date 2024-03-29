import pytest
from nycTaxis import dataHandler
from nycTaxis import core
import pandas as pd
import numpy as np
import os
import itertools

def test_numbers():
	assert 1+1 == 2


def notTest_saveAndLoad():

	testDf = pd.DataFrame(np.random.randint(0,100,size=(100, 4)), columns=list('ABCD'))
	dataHandler.saveDataFrame(testDf, './data.h5')
	loadedDf = dataHandler.loadDataFrame('./data.h5')

	os.remove('./data.h5')
	assert testDf.equals(loadedDf)


def test_AverageMonthNaive():

	averageNaive = core.averageMonthNaive('/home/tobi/Projects/BlueYonder/testData/yellow_testdata_2018-01.csv')
	dataFrame = dataHandler.loadFile('/home/tobi/Projects/BlueYonder/testData/yellow_testdata_2018-01.csv')
	averageNormal = core.averageMonth(dataFrame, 2018, 1)
	assert averageNaive == 60
	assert averageNaive == averageNormal


def test_validateBad():

	teststringsBad = ["2017-01-04", "notADate", "2019-99-99"]

	testDataFrame = dataHandler.loadFile('/home/tobi/Projects/BlueYonder/testData/yellow_testdata_2018-01.csv')
	testDataFrame, _ = dataHandler.calculateRollingAverage(testDataFrame)

	with pytest.raises(ValueError) as v:
		core.rollingAverageDate(testDataFrame, teststringsBad[0])
	assert 'not part of dataset' in str(v.value)

	with pytest.raises(ValueError) as v:
		core.rollingAverageDate(testDataFrame, teststringsBad[1])
	assert 'Incorrect Date Format' in str(v.value)

	with pytest.raises(ValueError) as v:
		core.rollingAverageDate(testDataFrame, teststringsBad[2])
	assert 'Incorrect Date Format' in str(v.value)


def test_validateGood():
	testStringGood = ['2018-01-01', '2018-02-01', '2018-01-02']

	for s in testStringGood:
		core._validate(s)


def test_condenseData():

	testDataFrame = dataHandler.loadFileRaw('/home/tobi/Projects/BlueYonder/testData/yellow_testdata_2018-01.csv')
	otherFrame = pd.read_csv('/home/tobi/Projects/BlueYonder/testData/yellow_testdata_2018-01.csv')

	# test if the one datapoint outside january 2018 gets removed
	assert testDataFrame.shape[0] == otherFrame.shape[0] - 1

	# test if it correctly falls into two single days
	condensedDataFrame = dataHandler.condenseData(testDataFrame)
	assert condensedDataFrame.shape[0] == 2
	assert condensedDataFrame['count'].loc['2018-01-01'] == 12
	assert condensedDataFrame['count'].loc['2018-01-02'] == 1

	#simple rolling average test
	condensedDataFrame_withAvg, _ = dataHandler.calculateRollingAverage(condensedDataFrame)
	assert np.isnan(core.rollingAverageDate(condensedDataFrame_withAvg, '2018-01-01'))

	condensedDataFrame_withAvg_appended = dataHandler.appendDataFrame(condensedDataFrame_withAvg,
	                                        '/home/tobi/Projects/BlueYonder/testData/yellow_testdata_2018-03.csv')
	assert condensedDataFrame_withAvg_appended.shape == (60, 3)


def test_workflow():
	dataPath = ['/home/tobi/Projects/BlueYonder/testData/yellow_testdata_2018-01.csv',
	            '/home/tobi/Projects/BlueYonder/testData/yellow_testdata_2018-02.csv',
				'/home/tobi/Projects/BlueYonder/testData/yellow_testdata_2018-03.csv']

	resultDataFrames = []

	#test if adding months in different order changes result (it should not)
	for subset in itertools.combinations(dataPath, len(dataPath)):
		dataFrameTotal = pd.DataFrame(columns=['duration', 'count'])
		for element in subset:
			dataFrameTotal = dataHandler.appendDataFrame(dataFrameTotal, element)
		resultDataFrames.append(dataFrameTotal)

	exampleDataFrame = resultDataFrames[0]
	for i in resultDataFrames:
		assert exampleDataFrame.equals(i)

	assert exampleDataFrame.shape[0] == 60  # 31 days in jan, 28 in Feb and 1 in March
	assert exampleDataFrame['rollingAvg'].iloc[-1] == 60  # every single datapoint in the testdata has duration 60 seconds

	assert exampleDataFrame['rollingAvg'].equals(core.rollingAverageTotal(exampleDataFrame))
