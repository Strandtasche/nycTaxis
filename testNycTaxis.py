import pytest
from nycTaxis import dataHandler
from nycTaxis import core
import pandas as pd
import numpy as np
import os


def test_numbers():
	assert 1+1 == 2


def notTest_saveAndLoad():

	testDf = pd.DataFrame(np.random.randint(0,100,size=(100, 4)), columns=list('ABCD'))
	dataHandler.saveDataFrame(testDf, './data.h5')
	loadedDf = dataHandler.loadDataFrame('./data.h5')

	os.remove('./data.h5')
	assert testDf.equals(loadedDf)


def test_AverageMonthNaive():

	average = core.averageMonthNaive('/home/tobi/Projects/BlueYonder/testData/yellow_testdata_2018-01.csv')
	assert average == 60


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

	condensedDataFrame_withAvg, _ = dataHandler.calculateRollingAverage(condensedDataFrame)
	assert np.isnan(core.rollingAverageDate(condensedDataFrame_withAvg, '2018-01-01'))



#Test, der überprüft, dass der Average richtig berechnet wird

	#Test, der überprüft, dass die Daten richtig geladen werden

