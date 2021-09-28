#inporting libraries
import tweepy
import requests
import json
from datetime import datetime
import requests.auth
from requests_oauthlib import OAuth1
from oauthlib.oauth2 import BackendApplicationClient
from requests.auth import HTTPBasicAuth
from urllib.parse import quote_plus
import pandas as pd
from purgo_malum import client as client1
import csv
import boto3
import multiprocessing
import pytz
import colorama
from colorama import Fore
###################################################Configurations#####################################################################################################

#Twitter credentials
consumer_key = 'Fkq1YtWMXJfm7rqFQe6bUMKnk'
consumer_secret = 'tbQFEXaYskF6vfHMN0xpBhjuDGIYP6vpNk4TYEsbn3ETOj6YKY'
access_token = '1254116935006072833-4lYrmDIsHq9wbVan3VDtdzwkeWe6Nc'
access_token_secret = 'f9zpd5uYABZCiK28Cixp5kR3dy6bFbXybDfwiWRMFvaa3'

#AWS credentials
ACCESS_KEY="AKIAQI6GMTIGYNVJZOAQ"
SECRET_KEY="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"

#######################################AWS Clients#########################################################################################################3
client = boto3.client(
    'comprehend',
    aws_access_key_id=ACCESS_KEY,
    aws_secret_access_key=SECRET_KEY,
    region_name = 'us-west-2'
)

#######################################################################################################################################################################

# Authenticate to Twitter
def veryfyingUser():
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret )
    auth.set_access_token(access_token,access_token_secret)
    api = tweepy.API(auth)
    
    try:
        api.verify_credentials()
        print(Fore.GREEN +"Authentication OK")
         
    
    except:
        print(Fore.RED +"Error During Authentication")

    return api


#***************************************************************************************************************************************************************************


#Getting other informations of a user
def userInfo(api,screen_name):
    print(Fore.GREEN +"Starting User Data Extraction from Twitter...")

    user=api.get_user(screen_name=screen_name)  # fetching the user
    id= user.id_str
    
    followersCount= user.followers_count   # Number of followers of a user
    numberOfTweets = user.statuses_count   # Number of tweets by users
    location = user.location              # Location of a user if mentioned
    description = user.description         # Bio of a user
    twitterDate= user.created_at
    delta = datetime.now(pytz.utc) 
    twitterAge=delta-twitterDate # Age on twitter
    tweetData={}
    tweets = api.user_timeline(screen_name = screen_name,count=200)
    tweetsList = [tweet.text for tweet in tweets]
    tweetLikes=[tweet.favorite_count for tweet in tweets]
    totalLikes= sum(tweetLikes)
    tweetData['id']=id
    tweetData['followers']=followersCount
    tweetData['tweet_count']= numberOfTweets
    tweetData['location']=location
    tweetData['twitter_age']= str(twitterAge.days)+ ' days'
    tweetData['twitter_bio']= description
    tweetData['total_likes']= totalLikes
    print(Fore.YELLOW +"User Data Extraction from Twitter Completed!!!")
    return tweetData,tweetsList
    
#*****************************************************************************************************************************************************************************8

def multiProcessingTweets(tweet):
    try:
        positiveScore=0
        negativeScore=0
        lang_response = client.detect_dominant_language(Text=tweet)
        languages = lang_response['Languages']
        lang_code = languages[0]['LanguageCode']

        response = client.detect_sentiment(
                    Text=tweet, LanguageCode=lang_code)
        
        
        if(response['Sentiment']=='POSITIVE'):
            positiveScore+=1
        elif(response['Sentiment']=='NEGATIVE'):
            negativeScore+=1
            
        return positiveScore,negativeScore
    except Exception as e:
            return 0,0   


#********************Sentiment Analysis of the data****************************************************************************************************************************

def twitterSentimentAnalysis(tweetData,tweetList):
    print(Fore.GREEN +"Starting Sentiment Analysis of Tweets...")
    
    try:
        totalPositiveScore=0
        totalNegativeScore=0
        
        p = multiprocessing.Pool()
        result = p.map(multiProcessingTweets, tweetList)
            
        for r in result:
            totalPositiveScore+=r[0]
            totalNegativeScore+=r[1]

        positivityPercent= (totalPositiveScore/tweetData['tweet_count'])
        negativityPercent= (totalNegativeScore/tweetData['tweet_count'])
        
        return positivityPercent,negativityPercent
    except Exception as e:
            print(Fore.RED + str(e))
            return None,None    
    finally:
        print(Fore.YELLOW +"Sentiment Analysis of Tweets Completed!!!")


#*****************************************************************************************************************************************************************************************

def getTwitterData(username,analysis_data):
    print(Fore.GREEN +"STARTING TWITTER DATA ANALYSIS")

    
    api=veryfyingUser()
    tweetData,tweetList=userInfo(api, username)
    positivityPercent,negativityPercent=twitterSentimentAnalysis(tweetData,tweetList)

    tweetData['positivityScore']=positivityPercent
    tweetData['negativityScore']=negativityPercent
    
    analysis_data['twitter_data']=tweetData.copy()
    # print(Fore.GREEN +analysis_data)
    print(Fore.CYAN +"TWITTER DATA ANALYSIS COMPLETED")
    
    

#......................................................................................................................................

    
