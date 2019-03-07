#!/bin/dev/env python
#Job to pull historical data from DarkSky API

import datetime
import time
import forecastio
from credentials import *

def pullDarkSkyData(myLat, myLong, pullDate):
  forecast = forecastio.load_forecast(darkSkyKey, myLat, myLong, time=pullDate)
  dayDetails = forecast.daily()
  return dayDetails

def fileWrite(row, fileName):
  filePath = "/home/gbk/data/weatherTracker/darkSky/"
  fullFileName = filePath + fileName
  delimiter = ","
  with open(fullFileName, 'a') as f:
      f.write(delimiter.join(row).encode('utf-8') + '\n')

def writePrecipFile(dayDetails, theYear):
  row = []
  precipFile = str(theYear) + "darkSkyPrecip.txt"
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
  fileWrite(row, precipFile)

def writeTempsFile(dayDetails, theYear):
  row = []
  tempsFile = str(theYear) + "darkSkyTemps.txt"
  for dataPoint in dayDetails.data:
    row.append(str(dataPoint.time))
    row.append(dataPoint.summary)
    row.append(dataPoint.icon)
    row.append(str(dataPoint.sunriseTime))
    row.append(str(dataPoint.sunsetTime))
    row.append(str(dataPoint.moonPhase))
    row.append(str(dataPoint.temperatureHigh))
    row.append(str(dataPoint.temperatureHighTime))
    try:
      row.append(str(dataPoint.temperatureLow))
    except:
      row.append('na')
    try:
      row.append(str(dataPoint.temperatureLowTime))
    except:
      row.append('na')
    row.append(str(dataPoint.apparentTemperatureHigh))
    row.append(str(dataPoint.apparentTemperatureHighTime))
    try:
      row.append(str(dataPoint.apparentTemperatureLow))
    except:
      row.append('na')
    try:
      row.append(str(dataPoint.apparentTemperatureLowTime))
    except:
      row.append('na')
    row.append(str(dataPoint.dewPoint))
    row.append(str(dataPoint.humidity))
    row.append(str(dataPoint.pressure))
    row.append(str(dataPoint.temperatureMax))
    row.append(str(dataPoint.temperatureMaxTime))
    row.append(str(dataPoint.temperatureMin))
    row.append(str(dataPoint.temperatureMinTime))
    row.append(str(dataPoint.apparentTemperatureMax))
    row.append(str(dataPoint.apparentTemperatureMaxTime))
    row.append(str(dataPoint.apparentTemperatureMin))
    row.append(str(dataPoint.apparentTemperatureMinTime))
  fileWrite(row, tempsFile)

def writeGreenEnergyFile(dayDetails, theYear):
  row = []
  greenFile = str(theYear) + "darkSkyGreenEnergy.txt"
  for dataPoint in dayDetails.data:
    row.append(str(dataPoint.time))
    row.append(str(dataPoint.windSpeed))
    row.append(str(dataPoint.windBearing))
    row.append(str(dataPoint.cloudCover))
    row.append(str(dataPoint.uvIndex))
    row.append(str(dataPoint.uvIndexTime))
    row.append(str(dataPoint.visibility))
  fileWrite(row, greenFile)

def cycleDaysOfYear(leapYear, theYear, myLat, myLong):
  for i in range(1, 366 + leapYear):
    pullDate = datetime.datetime.strptime(str(theYear) + str(i).zfill(3),
               "%Y%j")
    dayDetails = pullDarkSkyData(myLat, myLong, pullDate)
    writePrecipFile(dayDetails, theYear)
    writeTempsFile(dayDetails, theYear)
    writeGreenEnergyFile(dayDetails, theYear)

if __name__ == "__main__":
  myLat = 39.857979
  myLong = -89.544616
  leapYear = 0
  theYear = 2014
  cycleDaysOfYear(leapYear, theYear, myLat, myLong)
