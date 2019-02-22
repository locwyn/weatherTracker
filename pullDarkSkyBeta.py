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

def fileWrite(row, fileName):
  delimiter = ","
  with open(fileName, 'a') as f:
      f.write(delimiter.join(row) + '\n')

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
  precipFile = "darkSkyPrecip.txt"
  fileWrite(row, precipFile)

def writeTempFile(dayDetails):
  row = []
  tempFile = "darkSkyTemps.txt"
  for dataPoint in dayDetails.data:
    row.append(str(dataPoint.time))
    row.append(dataPoint.summary)
    row.append(dataPoint.dayIcon)
    row.append(str(dataPoint.sunriseTime))
    row.append(str(dataPoint.sunsetTime))
    row.append(str(dataPoint.moonPhase))
    row.append(str(dataPoint.temperatureHigh))
    row.append(str(dataPoint.temperatureHighTime))
    row.append(str(dataPoint.temperatureLow))
    row.append(str(dataPoint.temperatureLowTime))
    row.append(str(dataPoint.apparentTemperatureHigh))
    row.append(str(dataPoint.apparentTemperatureHighTime))
    row.append(str(dataPoint.apparentTemperatureLow))
    row.append(str(dataPoint.apparentTemperatureLowTime))
    row.append(str(datePoint.dewPoint))
    row.append(str(datePoint.humidty))
    row.append(str(datePoint.pressure))
    row.append(str(dataPoint.temperatureMax))
    row.append(str(dataPoint.temperatureMaxTime))
    row.append(str(dataPoint.temperatureMin))
    row.append(str(dataPoint.temperatureMinTime))
    row.append(str(dataPoint.apparentTemperatureMax))
    row.append(str(dataPoint.apparentTemperatureMaxTime))
    row.append(str(dataPoint.apparentTemperatureMin))
    row.append(str(dataPoint.apparentTemperatureMinTime))
  fileWrite(row, tempFile)


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
