#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
from nycTaxis import core
from nycTaxis import dataHandler


assert len(sys.argv) == 2, "Usage: 1. Argument - target date, rolling average"
targetDate = sys.argv[1]


taxiDataFrame = dataHandler.loadDataFrame('/home/tobi/Projects/BlueYonder/etc/data.h5')
result = core.rollingAverageDate(taxiDataFrame, targetDate)
print("the average drive length of the 45 days prior to and including {} was {}".format(targetDate, result))
