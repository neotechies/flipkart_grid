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

#Getting the user id

def getUser(api,userName):
    user = api.get_user(userName)
    return user.id_str

id=getUser(api,'mbcse50')


#Getting other informations of a user
def userInfo(api,id):
    user=api.get_user(id)  # fetching the user
    followersCount= user.followers_count   # Number of followers of a user
    numberOfTweets = user.statuses_count   # Number of tweets by users
    location = user.location              # Location of a user if mentioned
    description = user.description         # Bio of a user
    return followersCount,numberOfTweets,location
followersCount,numberOfTweets,location=userInfo(api,id)
print(followersCount)
print(numberOfTweets)
print(location)



def get_all_tweets(screen_name,api):
    #Twitter only allows access to a users most recent 3240 tweets with this method
  
    #initialize a list to hold all the tweepy Tweets
    alltweets = []  
    
    #make initial request for most recent tweets (200 is the maximum allowed count)
    new_tweets = api.user_timeline(screen_name = screen_name,count=200)
    
    #save most recent tweets
    alltweets.extend(new_tweets)
    
    #save the id of the oldest tweet less one
    oldest = alltweets[-1].id - 1
    
    #keep grabbing tweets until there are no tweets left to grab
    while len(new_tweets) > 0:
        
        #all subsiquent requests use the max_id param to prevent duplicates
        new_tweets = api.user_timeline(screen_name = screen_name,count=200,max_id=oldest)
        
        #save most recent tweets
        alltweets.extend(new_tweets)
        
        #update the id of the oldest tweet less one
        oldest = alltweets[-1].id - 1
        
    
    #transform the tweepy tweets into a 2D array that will populate the csv 
    outtweets = [[tweet.id_str, tweet.text,tweet.favorite_count] for tweet in alltweets]
    
    #Coverting the 2D data into dictionary
    column_names=['id','tweet','likes']
    tweetData={}
    for i in range(len(outtweets)):
        subTweets={}
        for j in range(len(outtweets[i])):
            subTweets[column_names[j]]=outtweets[i][j]
        tweetData[i]=subTweets
    
    print(json.dumps(tweetData,sort_keys=False,indent=2))
    #write the csv  
    # with open(f'new_{screen_name}_tweets.csv', 'w') as f:
    #     writer = csv.writer(f)
    #     writer.writerow(["id","created_at","text","Tweet_Likes"])
    #     writer.writerows(outtweets)
    
    # pass



get_all_tweets("mbcse50",api)