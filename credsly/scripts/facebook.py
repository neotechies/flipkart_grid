from zipfile import ZipFile
import os
import shutil
import json
import boto3
import glob
from purgo_malum import client as client1

ACCESS_KEY="AKIAQI6GMTIGYNVJZOAQ"
SECRET_KEY="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"

image_analysis_client = boto3.client(
    'rekognition',
    aws_access_key_id=ACCESS_KEY,
    aws_secret_access_key=SECRET_KEY,
)

text_analysis_client = boto3.client(
    'comprehend',
    aws_access_key_id=ACCESS_KEY,
    aws_secret_access_key=SECRET_KEY,
    region_name = 'us-west-2'
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
                 

def getFriendsCount(path):
    print("Starting Analysis Of Friend's Count...")
    try:
        f = open(path+"/friends_and_followers/friends.json",)
        data = json.load(f)
        return len(data['friends_v2'])
    except Exception as e:
        print("while Getting Friends Count for Facebook"+e)
        return None
    finally:    
        print("Analysis Of Friend's Count Completed")
       

def getReceivedFriendRequestsCount(path):
    print("Starting Analysis Of Friend Request's...")
    try:
        f = open(path+"/friends_and_followers/friend_requests_received.json",)
        data = json.load(f)
        return len(data['received_requests_v2'])
    except Exception as e:
        print("while Getting Friend Requests Count for Facebook"+e)
        return None
    finally:    
        print("Analysis Of Friend Request's Completed")
# def getGroupsDetails(path):
#     try:
#         f = open(path+"/groups/your_group_membership_activity.json",)
#         data = json.load(f)
#         return data['groups_joined_v2'] # Has to got for textanalsys
#     except Exception as e:
#         print("Error while Getting Groups Details Count for Facebook"+e)
#         return None


def getPageFollowedList(path):
    print("Starting Analysis Of Pages Followed...")
    try:
        f = open(path+"/pages/pages_you_follow.json",)
        totalPages = 0
        negativePages = 0
        data = json.load(f)
        for page_followed in data['pages_followed_v2']: # Has to got for textanalsys
            try:
                for page in page_followed['data']:
                    totalPages+=1
                    if(client1.contains_profanity(page['name'])):      #Checks for Bad words
                        negativePages+=1 
            except Exception as e:
                print(e)            

        return (negativePages,totalPages)
    except Exception as e:
        print(e)
        return None 
    finally:      
        print("Analysis Of Pages Followed Completed")

def getPageLikedList(path):
    print("Starting Analysis Of Pages Liked...")
    try:
        f = open(path+"/pages/pages_you've_liked.json",)
        data = json.load(f)
        totalPages = 0
        negativePages = 0
        for page in data['page_likes_v2']:
            totalPages+=1
            try:
                if(client1.contains_profanity(page['name'])):      #Checks for Bad words
                    negativePages+=1  
            except Exception as e:
                print(e)        
        #return data['page_likes_v2']
        # print(totalPages)
        # print(negativePages)
        return (negativePages,totalPages)
    except Exception as e:
        print(e)
        return None  
    finally:    
        print("Analysis Of Pages Liked Completed")

def getPageList(path):
    print("Starting Analysis Of Pages...")
    n1,t1 = getPageLikedList(path)
    n2,t2 = getPageFollowedList(path)  
    print("Analysis Of Pages Completed")  
    return (n1+n2)/(t1+t2)   
    


def getCommentsList(path):
    print("Starting Analysis Of Comments...")
    try:
        f = open(path+"/comments_and_reactions/comments.json",)
        data = json.load(f)
        positiveComments=0
        negativeComments=0
        totalComments=0
        for post in data['comments_v2']:
            try:
                for commentData in post['data']:
                    print(commentData['comment']['comment'])
                    totalComments+=1
                    lang_response = text_analysis_client.detect_dominant_language(Text=commentData['comment']['comment'])
                    languages = lang_response['Languages']
                    lang_code = languages[0]['LanguageCode']
                    response = text_analysis_client.detect_sentiment(Text=commentData['comment']['comment'], LanguageCode=lang_code)
                    print(response)
                    if(response['Sentiment']=='POSITIVE'):
                        positiveComments+=1
                    elif(response['Sentiment']=='NEGATIVE'):
                        negativeComments+=1
            except Exception as e:
                print(e)

        return positiveComments,negativeComments, totalComments

    except Exception as e:
        print(e)
        return None  
    finally:
        print("Analysis Of Comments Completed")
    
                       

def getPostsInteractionsCount(path):
    ## Likes Count
    print("Starting Analysis Of Posts...")
    try:
        f = open(path+"/comments_and_reactions/posts_and_comments.json",)
        data = json.load(f)
        print(data)
        return len(data['reactions_v2'])
    except Exception as e:
        print(e)
        return None    
    finally:
        print("Analysis Of Posts Completed")


def getProfileInfo(path):
    print("Starting Analysis Of Profile...")
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

        totalGroups = 0
        negativeGroups = 0
        for grp in data['groups']:
            print(grp['name'])
            totalGroups+=1
            if(client1.contains_profanity(grp['name'])):      #Checks for Bad words
                negativeGroups+=1
        profileInfo['negativeGroupPercentage'] = negativeGroups/totalGroups     

        return profileInfo

    except Exception as e:
        print(e)
        return None
    finally:
        print("Analysis Of Profile Completed") 

def getImageSentimentInfo(path):
    print("Starting Analysis Of Images Uploaded...") 
    try:
        extensions = ['*.gif', '*.png', '*.jpg', '*.jpeg']
        totalImages = 0
        negativeImages = 0
        for ext in extensions:
            for filename in glob.iglob(path+ '/**/'+ext, recursive=True):
                image = open(filename,'rb');
                image_read = image.read()
                totalImages+=1
                response = image_analysis_client.detect_moderation_labels(
                    Image={
                        'Bytes': image_read,
                    },
                )
                if(len(response['ModerationLabels'])>0):
                    negativeImages+=1
        return (negativeImages/totalImages)   
    except Exception as e:
        print(e)
        return None
    finally:
        print("Analysis Of Images Completed")

      

def getFacebookData(zipName, userID):
    # checkAndMakeDir(userID)
    # path="../userDataUploads/"+userID+"/facebook"
    # with ZipFile(file_name, 'r') as zip:
    #     # extracting all the files
    #     zip.extractall(path)
    totalFriends = getFriendsCount(path)
    totalFriendRequestRecieved = getReceivedFriendRequestsCount(path)
    negativePageListPercentage = getPageList(path)
    positiveComments,negativeComments, totalComments = getCommentsList(path)
    totalReactionsOnPost = getPostsInteractionsCount(path) #Likes and Comments
    totalNegativeImagesPercentage = getImageSentimentInfo(path)
    profileInfo = getProfileInfo(path)

getFacebookData("dadad","dada")  
