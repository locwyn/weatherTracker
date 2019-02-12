#!/bin/dev/env python
import datetime
import time

#testJulian = time.strptime("2019001", "%Y%j")
#print time.strftime("%Y_%m_%d", testJulian)

leapYear = 1
theYear = 2016
filePath = "/home/gbk/data/weatherTracker/"
for i in range(1, 366 + leapYear):
  fileDate = time.strftime("%Y_%m_%d", time.strptime(str(theYear) + str(i), "%Y%j"))
  fileName = fileDate + "_weather_obs.txt"
  fullFileName = filePath + fileName
  print(fullFileName)

"""
def testPoppin(arr1):
  arr1.pop(0)

arr1 = [1, 2, 3, 4, 5]

while len(arr1) > 0:
  testPoppin(arr1)
  print(arr1)
"""
