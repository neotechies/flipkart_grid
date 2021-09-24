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




#Twitter credentials
consumer_key = 'Fkq1YtWMXJfm7rqFQe6bUMKnk'
consumer_secret = 'tbQFEXaYskF6vfHMN0xpBhjuDGIYP6vpNk4TYEsbn3ETOj6YKY'
access_token = '1254116935006072833-4lYrmDIsHq9wbVan3VDtdzwkeWe6Nc'
access_token_secret = 'f9zpd5uYABZCiK28Cixp5kR3dy6bFbXybDfwiWRMFvaa3'

#AWS credentials
ACCESS_KEY="AKIAQI6GMTIGYNVJZOAQ"
SECRET_KEY="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"


client = boto3.client(
    'comprehend',
    aws_access_key_id=ACCESS_KEY,
    aws_secret_access_key=SECRET_KEY,
    region_name = 'us-west-2'
)

# Authenticate to Twitter
def veryfyingUser():
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret )
    auth.set_access_token(access_token,access_token_secret)
    api = tweepy.API(auth)
    
    try:
        api.verify_credentials()
        print("Authentication OK")
    except:
        print("Error during authentication")

    return api
api= veryfyingUser()




#Getting other informations of a user
def userInfo(api,screen_name):
    user=api.get_user(screen_name)  # fetching the user
    id= user.id_str
    followersCount= user.followers_count   # Number of followers of a user
    numberOfTweets = user.statuses_count   # Number of tweets by users
    location = user.location              # Location of a user if mentioned
    description = user.description         # Bio of a user
    twitterDate= user.created_at            # Age on twitter
    today = datetime.today()
    twitterAge=(today-twitterDate)
    tweetData={}
    tweets = api.user_timeline(screen_name = screen_name,count=200)
    tweetsList = [tweet.text for tweet in tweets]
    tweetLikes=[tweet.favorite_count for tweet in tweets]
    totalLikes= sum(tweetLikes)
    tweetData['id']=id
    tweetData['followers']=followersCount
    tweetData['tweet_count']= numberOfTweets
    tweetData['location']=location
    tweetData['twitter_age']= str(twitterAge)+ 'days'
    tweetData['twitter_bio']= description
    tweetData['total_likes']= totalLikes
    tweetData['tweets']= tweetsList
    return tweetData
tweetData=userInfo(api,'mbcse50')

#Sentiment Analysis of the data
def twitterSentimentAnalysis(tweetData):
    positiveScore=0
    negativeScore=0
    for i in range (len(tweetData['tweets'])):
        lang_response = client.detect_dominant_language(Text=tweetData['tweets'][i])
        languages = lang_response['Languages']
        lang_code = languages[0]['LanguageCode']

        response = client.detect_sentiment(
                    Text=tweetData['tweets'][i], LanguageCode=lang_code)
        
        
        if(response['Sentiment']=='POSITIVE'):
            positiveScore+=1
        elif(response['Sentiment']=='NEGATIVE'):
            negativeScore+=1

    positivityPercent= (positiveScore/tweetData['tweet_count'])*100
    negativityPercent= (negativeScore/tweetData['tweet_count'])*100
    return positivityPercent,negativityPercent
positivityPercent,negativityPercent= twitterSentimentAnalysis(tweetData)
print(positivityPercent,negativityPercent)


# if(client1.contains_profanity('You are an @a$$hole')):      #Checks for Bad words
#     print(True)

