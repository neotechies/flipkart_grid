#inporting libraries
import tweepy
import requests
import json
import requests.auth
from requests_oauthlib import OAuth1
from oauthlib.oauth2 import BackendApplicationClient
from requests.auth import HTTPBasicAuth
from urllib.parse import quote_plus
from pandas import DataFrame
import csv


#Function to convert credentials to access token

consumer_key = 'Fkq1YtWMXJfm7rqFQe6bUMKnk'
consumer_secret = 'tbQFEXaYskF6vfHMN0xpBhjuDGIYP6vpNk4TYEsbn3ETOj6YKY'
access_token = '1254116935006072833-4lYrmDIsHq9wbVan3VDtdzwkeWe6Nc'
access_token_secret = 'f9zpd5uYABZCiK28Cixp5kR3dy6bFbXybDfwiWRMFvaa3'


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
    tweetData={}
    tweets = api.user_timeline(screen_name = screen_name,count=200)
    tweetsList = [tweet.text for tweet in tweets]
    tweetLikes=[tweet.favorite_count for tweet in tweets]
    totalLikes= sum(tweetLikes)
    tweetData['id']=id
    tweetData['followers']=followersCount
    tweetData['tweet_count']= numberOfTweets
    tweetData['location']=location
    tweetData['twitter_bio']= description
    tweetData['total_likes']= totalLikes
    tweetData['tweets']= tweetsList
    return tweetData
tweetData=userInfo(api,'mbcse50')
print(json.dumps(tweetData,sort_keys=False,indent=2))


