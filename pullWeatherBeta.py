!/usr/bin/env python
import pyowm
import time

owm = pyowm.OWM('3cc9239f71004c1fa171a50d24e460e6')

"""
file structure
timeStamp,tempInFahrenheit['temp'],humidity,detailedStatus,rainVolume,wind-deg,wind-spe$
"""
def buildRow(owm):
    weatherRow = []
    observation = owm.weather_at_place('riverton,il')
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
    weatherRow.extend([str(timeStamp), str(tempInFahrenheit['temp']), str(humidity), de$
    weatherRow.extend([str(rainVolume), str(wind['deg']), str(wind['speed']), str(cloud$
    return weatherRow

theDate = time.strftime("%Y_%m_%d")
weatherFile = theDate + "_weather_obs.txt"
delimiter = ','
row = buildRow(owm)
with open(weatherFile, 'a') as outFile:
    outFile.write(delimiter.join(row) + '\n')

