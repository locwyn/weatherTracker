#!/usr/bin/env python

#job to load data from a year's worth of flat files into DB
import datetime
from datetime import timedelta
import time
import mysql.connector
from credentials import *

def databaseConnect():
  return mysql.connector.connect(user=dbUser, password=dbPassword,
           host=dbHost, database='weatherData')

def bulkLoadforYear(theYear, leapYear):
  filePath = "/home/gbk/data/weatherTracker/"
  for i in range(1, 366 + leapYear):
    fileDate = time.strftime("%Y_%m_%d", time.strptime(str(theYear) + str(i), "%Y%j"))
    fileName = fileDate + "_weather_obs.txt"
    fullFileName = filePath + fileName
    tableName = "test_owm_data"
    recList = readFileIntoList(fullFileName)
    for j in recList:
      splitRec = j.split(',')
      loadRecordIntoDatabase(tableName, parseFileRecords(splitRec))

def readFileIntoList(fullFileName):
  with open(fullFileName) as dataFile:
    recList = [line.rstrip("\n") for line in open(fullFileName)]
    return recList

def parseFileRecords(splitRec):
  timeStamp = float(splitRec[0])
  temp = float(splitRec[1])
  humidity = int(splitRec[2])
  detailedStatus = str(splitRec[3])
  rainVol = float(splitRec[4])
  windDeg = int(round(float(splitRec[5])))
  windSpeed = float(splitRec[6])
  clouds = int(splitRec[7])
  values = (timeStamp, temp, humidity,
            detailedStatus, rainVol,
            windDeg, windSpeed, clouds)
  return values

def loadRecordIntoDatabase(tableName, recList):
  values = parseFileRecords(recList)
  cnx = databaseConnect()
  cursor = cnx.cursor()
  recQuery = ("INSERT INTO " + tableName +
                " (timeStamp, tempInFahrenheit, "
                "humidity, detailedStatus, rainVolume, "
                "windDirection, windSpeed, clouds) "
                "VALUES (%s, %s, %s, %s, %s, %s, %s, %s)")
  try:
    cursor.execute(recQuery, values)
    cnx.commit()
    cnx.close()
  except mysql.connector.Error as e:
    writeErrorLog(e)

def writeErrorLog(e):
  filePath = '/home/gbk/data/weatherTracker/logs/'
  errorFile = (filePath + datetime.datetime.now().strftime('%Y_%m_%d') +
              '_error.log')
  try:
    with open(errorFile, 'a') as f:
      f.write(str(e) + "\n")
  except BaseException as e:
    with open(errorFile, 'a') as f:
      f.write("Unable to write error\n")

if __name__ == "__main__":
  theYear = 2018
  leapYear = 0
  bulkLoadForYear(theYear, leapYear)
