#!/usr/bin/env python
import time 
import datetime

def readFileIntoList(fileName):
  with open(fileName) as dataFile:
    recList = [line.rstrip("\n") for line in open(fileName)]
    return recList
        
def parseData(testData):
  for i in testData:
    splitRec = i.split(",")
    print(datetime.datetime.fromtimestamp(float(splitRec[0])).strftime('%H%M'))
    
    
#fileName = "2017_06_16_weather_obs_riv.txt"
#filePath = "/home/gbk/data/weatherTracker/oldOWMData/"
fileName = "seedStarterTemps20170616.txt"
filePath = "/home/gbk/data/weatherTracker/seedStarter/"
fullFileName = filePath + fileName

testData = readFileIntoList(fullFileName)
parseData(testData)
