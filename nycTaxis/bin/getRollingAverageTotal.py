#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
from nycTaxis import core
from nycTaxis import dataHandler


assert len(sys.argv) == 1, "Usage: no arguments"


taxiDataFrame = dataHandler.loadDataFrame('/home/tobi/Projects/BlueYonder/etc/data.h5')
result = core.rollingAverageTotal(taxiDataFrame)
if taxiDataFrame.duplicated().any():
	print("Warning: omitted some duplicates.")

print(result.to_string())

