#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
from nycTaxis import core
from nycTaxis import dataHandler


assert len(sys.argv) == 2, "Usage: 1. Argument - path to csv file or folder"
dataPath = sys.argv[1]

dataFrameTotal = dataHandler.loadDataFrame('/home/tobi/Projects/BlueYonder/etc/data.h5')

if os.path.exists(dataPath):
	dataFrameTotal = dataHandler.appendDataFrame(dataFrameTotal, dataPath)
	dataHandler.saveDataFrame(dataFrameTotal, '/home/tobi/Projects/BlueYonder/etc/data.h5')
else:
	print("Something is wrong with the given Argument")
	sys.exit(-1)


