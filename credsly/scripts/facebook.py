from zipfile import ZipFile
import os
import shutil
import json
import boto3

ACCESS_KEY="AKIAQI6GMTIGYNVJZOAQ"
SECRET_KEY="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"
client = boto3.client(
    'rekognition',
    aws_access_key_id=ACCESS_KEY,
    aws_secret_access_key=SECRET_KEY,
)



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

# def getGroupsDetails(path):
#     try:
#         f = open(path+"/groups/your_group_membership_activity.json",)
#         data = json.load(f)
#         return data['groups_joined_v2'] # Has to got for textanalsys
#     except Exception as e:
#         print("Error while Getting Groups Details Count for Facebook"+e)
#         return None

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

def getProfileInfo(path):
    try:
        f = open(path+"/profile_information/profile_information.json",)
        data = json.load(f)
        data=data['profile_v2']
        profileInfo={}
        profileInfo['name'] =data['name']['full_name']
        profileInfo['email'] =data['emails']['emails'][0]
        profileInfo['dob'] =str(data['birthday']['day'])+"/"+str(data['birthday']['month'])+"/"+str(data['birthday']['year'])
        profileInfo['gender'] =data['gender']['gender_option']
        profileInfo['relationship'] =data['relationship']['status']
        profileInfo['phone_verified'] =data['phone_numbers'][0]['verified']
        profileInfo['fb_registration'] =data['registration_timestamp']
        profileInfo['bio'] =data['intro_bio']['name']

        profileInfo['education_history'] = []
        for edu in data['education_experiences']:
            education={}
            education['place'] = edu['name']
            education['graduated'] = edu['graduated']
            if(len(edu['concentrations'])>0):
                education['type'] = edu['concentrations'][0]
            profileInfo['education_history'].append(education)

        profileInfo['groups'] = []
        for grp in data['groups']:
            profileInfo['groups'].append(grp['name'])    

        return profileInfo
    except Exception as e:
        print("Error "+e)
        return None


image = open(path+"/photos_and_videos/Coverphotos_2xJEHDkR2g/11407209_718802094913989_8372182250437187209_n_718802094913989.jpg", 'rb')
image_read = image.read()

response = client.detect_moderation_labels(
    Image={
        'Bytes': image_read,
    },
)

print(response)
      
