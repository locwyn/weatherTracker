#!/usr/bin/env python
import pyowm
import time

owm = pyowm.OWM('3cc9239f71004c1fa171a50d24e460e6')
filePath = "/home/gbk/data/weatherTracker/"
"""
file structure
timeStamp,tempInFahrenheit['temp'],humidity,detailedStatus,rainVolume,wind-deg,wind-spe$
GPS Coords for my house = 39.857979, -89.544616
"""
def buildRow(owm):
    weatherRow = []
    observation = owm.weather_at_coords(39.857979, -89.544616)
    w = observation.get_weather()
    tempInFahrenheit = w.get_temperature('fahrenheit')
    humidity = w.get_humidity()
    timeStamp = time.time()
    detailedStatus = w.get_detailed_status()
    rain = w.get_rain()
    try:
        rainVolume = rain['3h']
    except KeyError:
        rainVolume = 0
    wind = w.get_wind()
    clouds = w.get_clouds()
    weatherRow.extend([str(timeStamp), str(tempInFahrenheit['temp']), str(humidity), detailedStatus])
    weatherRow.extend([str(rainVolume), str(wind['deg']), str(wind['speed']), str(clouds)])
    return weatherRow

theDate = time.strftime("%Y_%m_%d")
weatherFile = filePath + theDate + "_weather_obs.txt"
delimiter = ','
row = buildRow(owm)
with open(weatherFile, 'a') as outFile:
    outFile.write(delimiter.join(row) + '\n')

