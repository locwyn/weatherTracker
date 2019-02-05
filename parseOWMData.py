#!/usr/bin/env python

filePath = "/home/gbk/data/weatherTracker/"
fileName = "2019_02_01_weather_obs.txt"
fullFileName = filePath + fileName

def readFileIntoList(fullFileName):
  with open(fullFileName) as dataFile:
    recList = [line.rstrip("\n") for line in open(fullFileName)]
    return recList

def parseFileRecords(recList):
  for i in recList:
    print(i)

if __name__ == "__main__":
  parseFileRecords(readFileIntoList(fullFileName))
