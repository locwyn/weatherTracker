#!/usr/bin/env python
import time 
import smtplib
from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText

s0Data = []
s1Data = []
s2Data = []
s3Data = []
s4Data = []
theDate = time.strftime("%Y%m%d")
fileName = "seedStarterTemps" + str(theDate) + ".txt"
msgBody = ""
msgSubject = "Seed Starter Temps for " + theDate

def readFileIntoList(fileName):
    with open(fileName) as dataFile:
        recList = [line.rstrip("\n") for line in open(fileName)]
        return recList

def parseData(testData):
  for i in testData:
    splitRec = i.split(",")
    s0Data.append((splitRec[0], splitRec[2], splitRec[3]))
    s1Data.append((splitRec[0], splitRec[5], splitRec[6]))
    s2Data.append((splitRec[0], splitRec[8], splitRec[9]))
    s3Data.append((splitRec[0], splitRec[11], splitRec[12]))
    s4Data.append((splitRec[0], splitRec[14], splitRec[15]))
    
def calcDailyAvg(sData):
  celAvg = 0.00
  fahAvg = 0.00
  for i in sData:
    celAvg += float(i[1])
    fahAvg += float(i[2])
  celAvg = celAvg / len(sData)
  fahAvg = fahAvg / len(sData)
  return (round(celAvg, 2), round(fahAvg, 2))
  
def calcDailyHighLow(sData):
  highCTemp = float(sData[0][1])
  lowCTemp = float(sData[0][1])
  highFTemp = float(sData[0][2])
  lowFTemp = float(sData[0][2])
  highTime = float(sData[0][0])
  lowTime = float(sData[0][0])
  for i in sData:
    if float(i[1]) >= highCTemp:
      highCTemp = float(i[1])
      highFTemp = float(i[2])
      highTime = float(i[0])
    if float(i[1]) <= lowCTemp:
      lowCTemp = float(i[1])
      lowFTemp = float(i[2])
      lowTime = float(i[0])
  return (highTime, round(highCTemp, 2), round(highFTemp, 2), lowTime, round(lowCTemp, 2), round(lowFTemp, 2))
  
def displayResults(sData, idNum):
  results = ""
  dailyAvg = calcDailyAvg(sData)
  dailyHighLow = calcDailyHighLow(sData)
  results += "Average Temp for sensor" + str(idNum) + " is: " + str(dailyAvg[1]) + "F.\n"
  results += "Daily Low Temp: " + str(dailyHighLow[5]) + "F at " + calcTime(dailyHighLow[3]) + "\n"
  results += "Daily High Temp: " + str(dailyHighLow[2]) + "F at " + calcTime(dailyHighLow[0]) + "\n\n"
  return results
  
def calcTime(utc):
  mkTime = time.localtime(utc)
  return time.strftime("%H:%M", mkTime)
  
def sendEmail(msgBody, msgSubject):
  fromaddr = "sinker78@gmail.com"
  toaddr = "gkresse@gmail.com"
  msg = MIMEMultipart()
  msg['From'] = fromaddr
  msg['To'] = toaddr
  msg['Subject'] = msgSubject
 
  body = msgBody
  msg.attach(MIMEText(body, 'plain'))
 
  server = smtplib.SMTP('smtp.gmail.com', 587)
  server.starttls()
  server.login(fromaddr, "z@r18gma78")
  text = msg.as_string()
  server.sendmail(fromaddr, toaddr, text)
  server.quit()


testData = readFileIntoList(fileName)
parseData(testData)
msgBody += displayResults(s0Data, 0)
msgBody += displayResults(s1Data, 1)
msgBody += displayResults(s2Data, 2)
msgBody += displayResults(s3Data, 3)
msgBody += displayResults(s4Data, 4)
sendEmail(msgBody, msgSubject)

