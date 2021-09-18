from zipfile import ZipFile
import os
import shutil
import json

file_name = "../userDataUploads/fbdata.zip"  #testing
userID= "mohit1234"
path="../userDataUploads/"+userID+"/facebook"


def checkAndMakeDir(userID):
    if(os.path.isdir("../userDataUploads/"+userID)):
        if(os.path.isdir("../userDataUploads/"+userID+"/facebook")):
            shutil.rmtree("../userDataUploads/"+userID+"/facebook")
            os.mkdir("../userDataUploads/"+userID+"/facebook") 
        else:
            os.mkdir("../userDataUploads/"+userID+"/facebook")   
    else:
        os.makedirs("../userDataUploads/"+userID+"/facebook")
                 
def getFacebookData(zipName, userID):
    checkAndMakeDir(userID)
    path="../userDataUploads/"+userID+"/facebook"
    with ZipFile(file_name, 'r') as zip:
        # extracting all the files
        
        zip.extractall(path)
  


def getFriendsCount(path):
    try:
        f = open(path+"/friends_and_followers/friends.json",)
        data = json.load(f)
        return len(data['friends_v2'])
    except Exception as e:
        print("Error while Getting Friends Count for Facebook"+e)
        return None

def getReceivedFriendRequestsCount(path):
    try:
        f = open(path+"/friends_and_followers/friend_requests_received.json",)
        data = json.load(f)
        return len(data['received_requests_v2'])
    except Exception as e:
        print("Error while Getting Friend Requests Count for Facebook"+e)
        return None

def getGroupsDetails(path):
    try:
        f = open(path+"/groups/your_group_membership_activity.json",)
        data = json.load(f)
        return data['groups_joined_v2'] # Has to got for textanalsys
    except Exception as e:
        print("Error while Getting Groups Details Count for Facebook"+e)
        return None

def getPageFollowedList(path):
    try:
        f = open(path+"/pages/pages_you_follow.json",)
        data = json.load(f)
        return data['pages_followed_v2'] # Has to got for textanalsys
    except Exception as e:
        print("Error "+e)
        return None   

def getPageLikedList(path):
    try:
        f = open(path+"/pages/pages_you've_liked.json",)
        data = json.load(f)
        return data['page_likes_v2'] # Has to got for textanalsys
    except Exception as e:
        print("Error "+e)
        return None  

def getCommentsList(path):
    try:
        f = open(path+"/comments_and_reactions/comments.json",)
        data = json.load(f)
        return data['comments_v2'], len(data['comments_v2']) # Has to got for textanalsys
    except Exception as e:
        print("Error "+e)
        return None          

def getPostsInteractionsCount(path):
    try:
        f = open(path+"/comments_and_reactions/posts_and_comments.json",)
        data = json.load(f)
        return len(data['reactions_v2'])
    except Exception as e:
        print("Error "+e)
        return None    



print(getPostsInteractionsCount(path))
      
