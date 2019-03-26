#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
from nycTaxis import core


assert len(sys.argv) == 2, "Usage: 1. Argument - path to csv file"
dataPath = sys.argv[1]


if os.path.isfile(dataPath):
	averageMonth = core.averageMonthNaive(dataPath)
	print("Average: {}".format(averageMonth))
else:
	print("File not found.")