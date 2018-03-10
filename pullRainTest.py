#!/usr/bin/env python
import pyowm
import time

owm = pyowm.OWM('3cc9239f71004c1fa171a50d24e460e6')

"""
file structure
timeStamp,rainVolume,rain,snow
"""
def buildRow(owm):
    weatherRow = []
    observation = owm.weather_at_place('riverton,il')
    w = observation.get_weather()
    timeStamp = time.time()
    rain = w.get_rain()
    try:
        rainVolume = rain['3h']
    except KeyError:
        rainVolume = 0
    snow = w.get_snow()
    weatherRow.extend([str(timeStamp), str(rainVolume), str(rain), str(snow)])
    return weatherRow


weatherFile = "pullRainData.txt"
delimiter = ','
row = buildRow(owm)
with open(weatherFile, 'a') as outFile:
    outFile.write(delimiter.join(row) + '\n')
