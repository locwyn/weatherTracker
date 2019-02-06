#!/usr/bin/env python
import json
import datetime
from datetime import timedelta
import mysql.connector
from credentials import *

def databaseConnect():
  return mysql.connector.connect(user=dbUser, password=dbPassword, 
           host=dbHost, database='weatherData')

def checkDatabaseForItem(selectQuery):
  cnx = databaseConnect()
  cursor = cnx.cursor()
  try:
    cursor.execute(selectQuery)
    results = 0
    for x in cursor:
      results += 1
    cnx.close()
  except mysql.connector.Error as e:
    writeErrorLog(e)
  return results

def loadTweetIntoDatabase(tweetJSON):
  selectQuery = "SELECT tweetID FROM tweets WHERE tweetID = " + str(tweetJSON['id'])
  if checkDatabaseForItem(selectQuery) == 0:
    values = pullTweetData(tweetJSON)
    cnx = databaseConnect()
    cursor = cnx.cursor()
    tweetQuery = ("INSERT INTO tweets "
                  "(tweetID, tweetText, user_id, "
                  "created_at, retweet_count) "
                  "VALUES (%s, %s, %s, %s, %s)")
    try:
      cursor.execute(tweetQuery, values)
      cnx.commit()
      cnx.close()
    except mysql.connector.Error as e:
      writeErrorLog(e)
      
def loadUserIntoDatabase(tweetJSON):
  selectQuery = "SELECT user_id FROM makers WHERE user_id = " + str(tweetJSON['user']['id'])
  if checkDatabaseForItem(selectQuery) == 0:
    values = pullMakerData(tweetJSON)
    cnx = databaseConnect()
    cursor = cnx.cursor()
    tweetQuery = ("INSERT INTO makers "
                  "(user_id, user_name, user_screen_name, "
                  "location, description, followers_count, "
                  "friends_count, created_at) "
                  "VALUES (%s, %s, %s, %s, %s, %s, %s, %s)")
    try:
      cursor.execute(tweetQuery, values)
      cnx.commit()
      cnx.close()
    except mysql.connector.Error as e:
      writeErrorLog(e)
    
def loadHashtagIntoDatabase(tag):
  values = (tag, 1)
  cnx = databaseConnect()
  cursor = cnx.cursor()
  tweetQuery = ("INSERT INTO hashtags "
                "(tags, total) "
                "VALUES (%s, %s)")
  try:
    cursor.execute(tweetQuery, values)
    cnx.commit()
    cnx.close()
  except mysql.connector.Error as e:
    writeErrorLog(e)
    
def updateHashtagTotals(tag):
  cnx = databaseConnect()
  cursor = cnx.cursor()
  tweetQuery = ("UPDATE hashtags SET "
                "total = total + 1 "
                "WHERE tags = \'" + tag + "\'")
  try:
    cursor.execute(tweetQuery)
    cnx.commit()
    cnx.close()
  except mysql.connector.Error as e:
    writeErrorLog(e)
    
def checkForEnglish(tweetJSON):
  if tweetJSON['lang'] == "en":
    return True
  else:
    return False

#need to set a minimum threshold for popularity
#def checkFollowerCount(tweetJSON):
#  return

#def collectHashtags(tweetJSON):
#  return

def pullTweetData(tweetJSON):
  tweetID = tweetJSON['id']
  tweetText = tweetJSON['text']
  userID = tweetJSON['user']['id']
  createdAt = tweetJSON['created_at']
  retweetCount = tweetJSON['retweet_count']
  tweetData = (tweetID, tweetText, userID, createdAt,
               retweetCount)
  return tweetData

def pullMakerData(tweetJSON):
  userID = tweetJSON['user']['id']
  userName = tweetJSON['user']['name']
  userScreenName = tweetJSON['user']['screen_name']
  location = tweetJSON['user']['location']
  description = tweetJSON['user']['description']
  followersCount = tweetJSON['user']['followers_count']
  friendsCount = tweetJSON['user']['friends_count']
  createdAt = tweetJSON['user']['created_at']
  makerData = (userID, userName, userScreenName, location,
               description, followersCount, friendsCount,
               createdAt)
  return makerData
  
def processHashtagData(tweetJSON):
  numHashtags = len(tweetJSON['entities']['hashtags'])
  hashtags = []
  if numHashtags == 0:
    pass
  else:
    for x in range(0, numHashtags):
      tag = tweetJSON['entities']['hashtags'][x]['text'].lower()
      selectQuery = "SELECT id FROM hashtags WHERE tags = \'" + tag + "\'"
      if checkDatabaseForItem(selectQuery) == 0:
        loadHashtagIntoDatabase(tag)
      else:
        updateHashtagTotals(tag)

def writeErrorLog(e):
  filePath = '/home/gbk/data/makerScrape/logs/'
  errorFile = (filePath + datetime.datetime.now().strftime('%Y_%m_%d') + 
              '_error.log')
  try:
    with open(errorFile, 'a') as f:
      f.write(str(e))
  except BaseException as e:
    with open(errorFile, 'a') as f:
      f.write("Unable to write error")
        
if __name__ == "__main__":
  filePath = '/home/gbk/data/makerScrape/'
  previousDate = datetime.datetime.now() - timedelta(days=1)
  fileName = (filePath + previousDate.strftime('%Y_%m_%d') 
             + '_maker.json')
  with open(fileName) as f:
    tweets = f.readlines()
  for y in tweets:
    tweetJSON = json.loads(y)
    if tweetJSON.get('retweeted_status'):
      pass
    else:
      if checkForEnglish(tweetJSON):
        loadTweetIntoDatabase(tweetJSON)
        loadUserIntoDatabase(tweetJSON)
        processHashtagData(tweetJSON)
