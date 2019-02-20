#!/bin/dev/env python
#Job to pull historical data from DarkSky API

import datetime
import time
import forecastio
from credentials import *
#testJulian = time.strptime("2019001", "%Y%j")
#print time.strftime("%Y_%m_%d", testJulian)

def pullDarkSkyData(myLat, myLong, pullDate):
  forecast = forecastio.load_forecast(darkSkyKey, myLat, myLong, time=pullDate)
  byDay = forecast.daily()
  for dataPoint in byDay.data:
    print dataPoint.time
    print dataPoint.summary
    print dataPoint.icon
    print dataPoint.sunriseTime
    print dataPoint.sunsetTime
    print dataPoint.moonPhase
    print dataPoint.temperatureHigh

#def writePrecipFile():

#def writeTempFile():

#def writeGreenEnergyFile():

def cycleDaysOfYear(leapYear, theYear, filePath, myLat, myLong):
  for i in range(1, 366 + leapYear):
    fileDate = time.strftime("Y_%m_%d", time.strptime(str(theYear) + str(i),
                             "%Y_%j"))
    fileName = fileDate + "_darkSkyData.txt"

if __name__ == "__main__":
  myLat = 39.857979
  myLong = -89.544616
  leapYear = 0
  theYear = 2018
  pullDate = datetime.datetime(2019, 01, 01)
  filePath = "/home/gbk/data/weatherTracker/"
  pullDarkSkyData(myLat, myLong, pullDate)
