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
  dayDetails = forecast.daily()
  return dayDetails

def writePrecipFile(dayDetails):
  row = []
  for dataPoint in dayDetails.data:
    row.append(str(dataPoint.time))
    row.append(str(dataPoint.precipIntensity))
    row.append(str(dataPoint.precipIntensityMax))
    try:
      row.append(str(dataPoint.precipIntensityMaxTime))
    except:
      row.append("0")
    row.append(str(dataPoint.precipProbability))
    try:
      row.append(str(dataPoint.precipAccumulation))
    except:
      row.append("0")
    try:
      row.append(str(dataPoint.precipType))
    except:
      row.append("None")
  #row.extend([dayPrecipIntensity, dayPrecipIntensityMax])
  #row.extend([dayPrecipIntensityMaxTime, dayPrecipProbability])
  #row.extend([dayPrecipAccumulation, dayPrecipType])
  delimiter = ","
  precipFile = "darkSkyPrecip.txt"
  with open(precipFile, 'a') as pf:
      pf.write(delimiter.join(row) + '\n')

def writeTempFile(dayDetails):
  for dataPoint in dayDetails.data:
    dayTime = str(dataPoint.time)
    daySummary = dataPoint.summary
    dayIcon = dataPoint.dayIcon
    daySunriseTime = str(dataPoint.sunriseTime)
    daySunsetTime = str(dataPoint.sunsetTime)
    dayMoonPhase = str(dataPoint.moonPhase)
    dayTemperatureHigh = str(dataPoint.temperatureHigh)
    dayTemperatureHighTime = str(dataPoint.temperatureHighTime)
    dayTemperatureLow = str(dataPoint.temperatureLow)
    dayTemperatureLowTime = str(dataPoint.temperatureLowTime)
    dayAppTemperatureHigh = str(dataPoint.apparentTemperatureHigh)
    dayAppTemperatureHighTime = str(dataPoint.apparentTemperatureHighTime)
    dayAppTemperatureLow = str(dataPoint.apparentTemperatureLow)
    dayAppTemperatureLowTime = str(dataPoint.apparentTemperatureLowTime)
    


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
  pullDate = datetime.datetime(2019, 01, 11)
  filePath = "/home/gbk/data/weatherTracker/"
  dayDetails = pullDarkSkyData(myLat, myLong, pullDate)
  writePrecipFile(dayDetails)
