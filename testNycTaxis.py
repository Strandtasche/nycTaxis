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

	average = core.averageMonthNaive('/home/tobi/Projects/BlueYonder/testData/testData01.csv')
	assert average == 60







	#Test, der überprüft, dass der Average richtig berechnet wird

	#Test, der überprüft, dass die Daten richtig geladen werden

