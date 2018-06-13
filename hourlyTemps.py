#!/usr/bin/env python
import time 
import datetime

def readFileIntoList(fileName):
  with open(fileName) as dataFile:
    recList = [line.rstrip("\n") for line in open(fileName)]
    return recList
        
def parseData(testData):
  numRecs = 0
  sumOfTemps = 0
  averageTempForDay = 0
  for i in testData:
    splitRec = i.split(",")
    #print(datetime.datetime.fromtimestamp(float(splitRec[0]) - 18000).strftime('%c') + " : " + splitRec[3])
    #print(datetime.datetime.fromtimestamp(float(splitRec[0])).strftime('%H%M') + ":" + splitRec[1])
    try:
      sumOfTemps += float(splitRec[1])
      numRecs += 1
    except:
      pass
  if numRecs > 0:
    averageTempForDay = sumOfTemps / numRecs
  return round(averageTempForDay, 2)
 
def loopDateRange():
  for i in range(60, 208):
    processJulianDate = "2017" + str(i)
    processRegDate = time.strftime("%Y_%m_%d", time.strptime(processJulianDate, "%Y%j"))
    fileName = processRegDate + "_weather_obs_riv.txt"
    filePath = "/home/gbk/data/weatherTracker/oldOWMData/"
    #fileName = "seedStarterTemps20170616.txt"
    #filePath = "/home/gbk/data/weatherTracker/seedStarter/"
    fullFileName = filePath + fileName
    print(processRegDate + " - " + str(parseData(readFileIntoList(fullFileName))))

#testData = readFileIntoList(fullFileName)
#print(parseData(testData))

if __name__ == "__main__":
  loopDateRange()
