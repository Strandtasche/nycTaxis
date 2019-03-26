#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
from nycTaxis import core
from nycTaxis import dataHandler


assert len(sys.argv) == 2, "Usage: 1. Argument - path to csv file or folder"
dataPath = sys.argv[1]

if os.path.isdir(dataPath):
	dataFrameTotal = dataHandler.loadFolder(dataPath)
elif os.path.isfile(dataPath):
	dataFrameTotal = dataHandler.loadFileRaw(dataPath)
else:
	print("Something is wrong with the given Argument")
	sys.exit(-1)

print("calculating rolling average...")
dataFrameTotal, _ = core.calculateRollingAverage(dataFrameTotal)
dataHandler.saveDataFrame(dataFrameTotal, '/home/tobi/Projects/BlueYonder/etc/data.h5')
print("done, and saved")
