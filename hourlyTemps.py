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
    print(splitRec[0])
    
fileName = "2017_06_16_weather_obs_riv.txt"
filePath = "/home/gbk/data/weatherTracker/oldOWMData/"
fullFileName = filePath + fileName

testData = readFileIntoList(fullFileName)
parseData(testData)
