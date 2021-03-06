'''
Created on 8-mei-2013

@author: Brecht Deconinck
'''
import Methods.IO as IO
from Classes import Tweet
from stemming.porter2 import stem
from datetime import datetime, timedelta
from decimal import *

def main():
    #classifyTweetsCompany("AAPL")
    classifyTweetsDJIA(3)
    
def classifyTweets(tweetFile, history, tag, sSaveFile, offset=3):
    stopWords = getStopWords()
    tweets = []    
    for line in IO.readData_by_line(tweetFile):
        tweet = Tweet.Tweet()
        tweet.setTweet(line)
        if(tweet.containsTag("#" + tag)):
            stamp = tweet.date + timedelta(days=offset)
            if stamp.date() in history:
                tweet.label = history[stamp.date()]
                tweet.removeStopWords(stopWords)
                tweets.append(tweet)
    print len(tweets)
    tweetFile.close()
    IO.writeTweets(sSaveFile, tweets, ['label', 'trimmedMessage'])
    
def classifyTweetsDJIA(_offset=3):
    tweetFile = open("data/scrapeDJIA.txt")
    priceData = IO.readData("data/DJIA.tsv")
    priceHist = priceHistory(priceData, "%b %d, %Y", 1)
    
    classifyTweets(tweetFile, priceHist, "DJIA", "data/ClassifiedDJIA.txt", offset=_offset)
#     # TODO: Read last line of classified tweets
#     data = IO.readData("data/DJIA.tsv")
#     history = priceHistory(data, "%b %d, %Y", 1)
#     tweetFile = open("data/scrapeDJIA.txt")
#     tweets = []    
#     for line in IO.readData_by_line(tweetFile):
#         tweet = Tweet.Tweet()
#         tweet.setTweet(line)
#         tweet.label = history[tweet.date.date()]
#         tweets.append(tweet)        
#     IO.writeTweets("data/ClassifiedDJIA.txt", tweets, ['label', 'trimmedMessage'])
    
def classifyTweetsCompany(tag, _offset=3):
    tweetFile = open("data/scrapeCompanies.txt")
    priceData = IO.readData("data/" + tag + ".csv", ',')
    priceIter = iter(priceData)
    next(priceIter)
    priceHist = priceHistory(priceIter, "%Y-%m-%d", 2)
    
    classifyTweets(tweetFile, priceHist, tag, "data/Classified" + tag + ".txt", offset=_offset)
#     # TODO: Read last line of classified tweets
#     data = IO.readData("data/" + tag + ".csv", ',')
#     iterData = iter(data)
#     next(iterData)
#     
#     stopWords = getStopWords()
#     
#     history = priceHistory(iterData, "%Y-%m-%d", 2)
#     tweetFile = open("data/scrapeCompanies.txt")
#     tweets = []    
#     for line in IO.readData_by_line(tweetFile):
#         tweet = Tweet.Tweet()
#         tweet.setTweet(line)
#         if(tweet.containsTag("#" + tag)):
#             stamp = tweet.date + timedelta(days=4)
#             if stamp.date() in history:
#                 tweet.label = history[stamp.date()]
#                 tweet.removeStopWords(stopWords)
#                 tweets.append(tweet)
#         
#     tweetFile.close()
#     IO.writeTweets("data/Classified" + tag + ".txt", tweets, ['label', 'trimmedMessage'])


def priceHistory(data, sDateFormat, indexValue):    
    prices = {}
    first = True
    date = datetime.today()
    oldestPrintDT = date + timedelta(days=-21)
    lastDate = date
    
    for line in data:
        lastDate = datetime.strptime(line[0], sDateFormat)
        if first:
            date = lastDate
            first = False
        prices[lastDate] = Decimal(line[indexValue])
        
    priceChanges = {}
    priceChange = 0
    while (date > lastDate):
        nextDay = date + timedelta(days=-1)
        if date in prices:            
            while nextDay not in prices:
                nextDay = nextDay + timedelta(days=-1)            
            if (prices[date] - prices[nextDay] >= 0):
                priceChange = 1
            else:
                priceChange = 0
        priceChanges[date.date()] = priceChange
        
        # Print recent changes
#         if (date > oldestPrintDT):
#             print str(date.date()) + ": " + str(priceChange)
        date = date + timedelta(days=-1)

    return priceChanges
    
def setTweetsEmotion():
    #Get Emotions
    arrEmo = getEmotions()
    #Analyse Tweet Emotion
    data = open("data/scrapeCompanies.txt")    
    #Read every tweet
    for line in IO.readData_by_line(data):
        tweet = Tweet.Tweet()
        tweet.setTweet(line)
        #Check every emotion
        value = 0
        for emo in arrEmo:
            word = emo[0]
            if word in tweet.message:
                #Update value by emotion
                if emo[1] == "1":
                    value = 1
                else:
                    value = -1
                if(value != 0):
                    break
            tweet.label = value
        print tweet.label, " " ,tweet.message

def getEmotions():
    arr = IO.readData("data/Emotions.txt")
    for index in range(0, len(arr)):
        arr[index][0] = stem(arr[index][0])
    return arr

def getStopWords():
    arr = IO.readData("data/StopWords.txt")
    return arr

if __name__ == '__main__':
    main()