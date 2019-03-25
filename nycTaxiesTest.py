import pytest
from nycTaxis import dataHandler
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








	#Test, der überprüft, dass der Average richtig berechnet wird

	#Test, der überprüft, dass die Daten richtig geladen werden

