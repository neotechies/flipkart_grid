from zipfile import ZipFile
import os
import shutil
import json
import boto3
import glob
from purgo_malum import client as client1
import multiprocessing
from pathlib import Path
import colorama
from colorama import Fore


########################################################Configuration Keys#######################################################################################

ACCESS_KEY="AKIAQI6GMTIGYNVJZOAQ"
SECRET_KEY="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"

BASE_DIR = Path(__file__).resolve().parent.parent.parent

#####################################################AWS Clients###################################################################################

image_analysis_client = boto3.client(
    'rekognition',
    aws_access_key_id=ACCESS_KEY,
    aws_secret_access_key=SECRET_KEY,
    region_name = 'us-west-2'
)

text_analysis_client = boto3.client(
    'comprehend',
    aws_access_key_id=ACCESS_KEY,
    aws_secret_access_key=SECRET_KEY,
    region_name = 'us-west-2'
)

#################################################Variables For Testing###################################################################################

# file_name = "../userDataUploads/fbdata.zip"  #testing
# userID= "mohit1234"
# path="../../userDataUploads/"+userID+"/facebook"

######################################Checking and making directory for zip Extraction##########################################################

def checkAndMakeDir(userID):
    if(os.path.isdir(str(BASE_DIR)+"/userDataUploads/"+userID)):
        if(os.path.isdir(str(BASE_DIR)+"/userDataUploads/"+userID+"/facebook")):
            shutil.rmtree(str(BASE_DIR)+"/userDataUploads/"+userID+"/facebook")
            os.mkdir(str(BASE_DIR)+"/userDataUploads/"+userID+"/facebook") 
        else:
            os.mkdir(str(BASE_DIR)+"/userDataUploads/"+userID+"/facebook")   
    else:
        os.makedirs(str(BASE_DIR)+"/userDataUploads/"+userID+"/facebook")

#**********************************************************Friends Analysis**********************************************************************************                 

def getFriendsCount(path, fb_dict):
    print(Fore.GREEN+"Starting Analysis Of Friend's Count...")
    try:
        f = open(path+"/friends_and_followers/friends.json",)
        data = json.load(f)
        fb_dict['totalFriends'] = len(data['friends_v2'])
        #return len(data['friends_v2'])
    except Exception as e:
        print(Fore.RED +"while Getting Friends Count for Facebook"+ str(e))
        fb_dict['totalFriends'] = None
        #return None
    finally:    
        print(Fore.YELLOW +"Analysis Of Friend's Count Completed")

#*****************************************************Friend Requests Analysis*************************************************************************S      

def getReceivedFriendRequestsCount(path, fb_dict):
    print(Fore.GREEN+"Starting Analysis Of Friend Request's...")
    try:
        f = open(path+"/friends_and_followers/friend_requests_received.json",)
        data = json.load(f)
        fb_dict['totalFriendRequestsRecieved'] = len(data['received_requests_v2'])
        #return len(data['received_requests_v2'])
    except Exception as e:
        print(Fore.RED +"while Getting Friend Requests Count for Facebook"+ str(e))
        fb_dict['totalFriendRequestsRecieved'] = None
        #return None
    finally:    
        print(Fore.YELLOW +"Analysis Of Friend Request's Completed")

#************************************************Page Followed and Liked Analysis**********************************************************************************************************S

def pagefollow_multiprocessing(page_followed):
    totalPages = 0
    negativePages = 0
    try:
        for page in page_followed['data']:
            totalPages+=1
            if(client1.contains_profanity(page['name'])):      #Checks for Bad words
                negativePages+=1 
    except Exception as e:
        print(Fore.RED + str(e))            
    return negativePages, totalPages


def getPageFollowedList(path, sub_fb_dict):
    print(Fore.GREEN +"Starting Analysis Of Pages Followed...")
    try:
        f = open(path+"/pages/pages_you_follow.json",)
        totalPages = 0
        negativePages = 0
        data = json.load(f)
        p = multiprocessing.Pool() 
        result = p.map(pagefollow_multiprocessing, data['pages_followed_v2'])
        for r in result:
            negativePages+=r[0]
            totalPages+=r[1] 
        sub_fb_dict['n2']=negativePages
        sub_fb_dict['t2']=totalPages
        #return (negativePages,totalPages)
    except Exception as e:
        print(Fore.RED  + str(e))
        sub_fb_dict['n2'] = None
        sub_fb_dict['t2'] = None
        #return None 
    finally:      
        print(Fore.YELLOW +"Analysis Of Pages Followed Completed")

def pageliked_multiprocessing(page):
    totalPages =1
    negativePages = 0
    try:
        if(client1.contains_profanity(page['name'])):      #Checks for Bad words
            negativePages+=1  
    except Exception as e:
        print(Fore.RED + str(e))
    return negativePages, totalPages    

def getPageLikedList(path, sub_fb_dict):
    print(Fore.GREEN +"Starting Analysis Of Pages Liked...")
    try:
        f = open(path+"/pages/pages_you've_liked.json",)
        data = json.load(f)
        totalPages = 0
        negativePages = 0
        p = multiprocessing.Pool() 
        result = p.map(pageliked_multiprocessing,  data['page_likes_v2'])
        for r in result:
            negativePages+=r[0]
            totalPages+=r[1]        
        #return data['page_likes_v2']
        # print(Fore.GREEN +Fore.GREEN +totalPages)
        # print(Fore.GREEN +Fore.GREEN +negativePages)
        sub_fb_dict['n1']=negativePages
        sub_fb_dict['t1']=totalPages
        #return (negativePages,totalPages)
    except Exception as e:
        print(Fore.RED + str(e))
        sub_fb_dict['n1'] = None
        sub_fb_dict['t1'] = None
        #return None  
    finally:    
        print(Fore.YELLOW +"Analysis Of Pages Liked Completed")

def getPageList(path,fb_dict):
    print(Fore.GREEN+"Starting Analysis Of Pages...")
    manager = multiprocessing.Manager()
    sub_fb_dict = manager.dict()
    p1 = multiprocessing.Process(target=getPageLikedList, args=(path,sub_fb_dict ))
    p2 = multiprocessing.Process(target=getPageFollowedList, args=(path, sub_fb_dict))
    p1.start()
    p2.start()
    p1.join()
    p2.join()
    # n1,t1 = getPageLikedList(path)
    # n2,t2 = getPageFollowedList(path)  
    print(Fore.YELLOW +"Analysis Of Pages Completed")
    fb_dict['negativePageListPercentage'] = (sub_fb_dict['n1']+sub_fb_dict['n2'])/(sub_fb_dict['t1']+sub_fb_dict['t2'])
    #return (sub_fb_dict['n1']+sub_fb_dict['n2'])/(sub_fb_dict['t1']+sub_fb_dict['t2'])   

#**********************************Comments Analysis*********************************************************************    

def comment_array_multiprocess(post):
        positiveComments=0
        negativeComments=0
        totalComments=0

        try:
            for commentData in post['data']:
                lang_response = text_analysis_client.detect_dominant_language(Text=commentData['comment']['comment'])
                languages = lang_response['Languages']
                lang_code = languages[0]['LanguageCode']
                response = text_analysis_client.detect_sentiment(Text=commentData['comment']['comment'], LanguageCode=lang_code)
                totalComments+=1
                if(response['Sentiment']=='POSITIVE'):
                    positiveComments+=1
                elif(response['Sentiment']=='NEGATIVE'):
                    negativeComments+=1
        except Exception as e:
            return None, None, None
            #print(Fore.GREEN +Fore.GREEN +e)
        return positiveComments, negativeComments, totalComments



def getCommentsList(path, fb_dict):
    print(Fore.GREEN +"Starting Analysis Of Comments...")
    try:
        f = open(path+"/comments_and_reactions/comments.json",)
        data = json.load(f)
     
        positiveComments=0
        negativeComments=0
        totalComments=0

        p = multiprocessing.Pool() 
        result = p.map(comment_array_multiprocess, data['comments_v2'])
        for r in result:
            if(r[0]!=None):
                positiveComments+=r[0]
                negativeComments+=r[1]
                totalComments+=r[2]          
        fb_dict['positiveComments'] = positiveComments
        fb_dict['negativeComments'] = negativeComments
        fb_dict['totalComments'] = totalComments
        #return positiveComments,negativeComments, totalComments

    except Exception as e:
        print(Fore.RED + str(e))
        fb_dict['positiveComments'] = None
        fb_dict['negativeComments'] = None
        fb_dict['totalComments'] = None
        #return None  
    finally:
        print(Fore.YELLOW +"Analysis Of Comments Completed")

#**********************************Posts Analysis*********************************************************************    

def posts_multiprocess(post):
        positivePosts=0
        negativePosts=0
        totalPosts=0

        try:
            for data in post['data']:
                lang_response = text_analysis_client.detect_dominant_language(Text=data['post'])
                languages = lang_response['Languages']
                lang_code = languages[0]['LanguageCode']
                response = text_analysis_client.detect_sentiment(Text=data['post'], LanguageCode=lang_code)
                totalPosts+=1
                if(response['Sentiment']=='POSITIVE'):
                    positivePosts+=1
                elif(response['Sentiment']=='NEGATIVE'):
                    negativePosts+=1
        except Exception as e:
            return None, None, None
            #print(Fore.GREEN +Fore.GREEN +e)
        return positivePosts, negativePosts, totalPosts



def getPostsList(path, fb_dict):
    print(Fore.GREEN +"Starting Analysis Of Posts...")
    try:
        f = open(path+"/posts/your_posts_1.json",)
        data = json.load(f)
        positivePosts=0
        negativePosts=0
        totalPosts=0

        p = multiprocessing.Pool() 
        result = p.map(posts_multiprocess, data)
        for r in result:
            if(r[0]!=None):
                positivePosts+=r[0]
                negativePosts+=r[1]
                totalPosts+=r[2]          
        fb_dict['positivePosts'] = positivePosts/totalPosts
        fb_dict['negativePosts'] = negativePosts/totalPosts
        fb_dict['totalPosts'] = totalPosts
        # return positiveComments,negativeComments, totalComments

    except Exception as e:
        print(Fore.RED + str(e))
        fb_dict['positivePosts'] = None
        fb_dict['negativePosts'] = None
        fb_dict['totalPosts'] = None
        #return None  
    finally:
        print(Fore.YELLOW +"Analysis Of Posts Completed")

#************************************************Post's Interaction Analysis******************************************************************                       

def getPostsInteractionsCount(path, fb_dict):
    ## Likes Count
    print(Fore.GREEN +"Starting Analysis Of Posts...")
    try:
        f = open(path+"/comments_and_reactions/posts_and_comments.json",)
        data = json.load(f)
        fb_dict['totalReactionsOnPost'] = len(data['reactions_v2'])
        #return len(data['reactions_v2'])
    except Exception as e:
        print(Fore.RED + str(e))
        fb_dict['totalReactionsOnPost'] = None
        #return None    
    finally:
        print(Fore.YELLOW +"Analysis Of Posts Completed")

#*************************************************Analysis of groups Joined********************************************************************S
def groups_multiprocessing(grp):
    totalGroups = 1
    negativeGroups = 0
    if(client1.contains_profanity(grp['name'])):      #Checks for Bad words
        negativeGroups+=1
    return negativeGroups, totalGroups    

def getProfileInfo(path, fb_dict):
    print(Fore.GREEN +"Starting Analysis Of Profile...")
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

        p = multiprocessing.Pool() 
        result = p.map(groups_multiprocessing, data['groups'])
        for r in result:
            negativeGroups +=r[0]
            totalGroups +=r[1]     
               
        profileInfo['negativeGroupPercentage'] = negativeGroups/totalGroups     

        fb_dict['profileInfo'] = profileInfo
        #return profileInfo

    except Exception as e:
        print(Fore.RED + str(e))
        fb_dict['profileInfo'] = None
        #return None
    finally:
        print(Fore.YELLOW +"Analysis Of Profile Completed") 

#*******************************************************Analysis of Images Uploaded*****************************************************************************S
def image_multiprocessing(filename):
        try:
            totalImages = 1
            negativeImages = 0
            image = open(filename,'rb');
            image_read = image.read()
            response = image_analysis_client.detect_moderation_labels(
                Image={
                    'Bytes': image_read,
                },
            )
            # print(response)
            if(len(response['ModerationLabels'])>0):
                negativeImages+=1

            return negativeImages,totalImages  
        except Exception as e:
            # print(Fore.RED + str(e) +Fore.GREEN +" Forwarding to next Image")
            return 0,0      

def getImageSentimentInfo(path, fb_dict):
    print(Fore.GREEN +"Starting Analysis Of Images Uploaded...") 
    try:
        extensions = ['*.gif', '*.png', '*.jpg', '*.jpeg']
        totalImages = 0
        negativeImages = 0
        result=[]
        for ext in extensions:
            p = multiprocessing.Pool()
            sub_result= p.map(image_multiprocessing,glob.iglob(path+ '/**/'+ext, recursive=True))
            result+=sub_result
        
        for r in result:
            negativeImages+=r[0]
            totalImages+=r[1]
               
        fb_dict['totalNegativeImagesPercentage'] = (negativeImages/totalImages)           
        #return (negativeImages/totalImages)   
    except Exception as e:
        print(Fore.RED + str(e))
        fb_dict['totalNegativeImagesPercentage'] = None
        #return None
    finally:
        print(Fore.YELLOW +"Analysis Of Images Completed")



#*******************************
# ****************************************Main Function************************************************************      
#*******************************

def getFacebookData(zipName, userID, analysis_data):
    print(Fore.GREEN +"STARTING FACEBOOK DATA ANALYSIS")
    checkAndMakeDir(userID)
    path=str(BASE_DIR)+"/userDataUploads/"+userID+"/facebook"
    filename=str(BASE_DIR)+"/userDataUploads/ZIP_UPLOADS/"+zipName
    with ZipFile(filename, 'r') as zip:
        # extracting all the files
        zip.extractall(path)
    manager = multiprocessing.Manager()
    fb_dict = manager.dict()
    p1 = multiprocessing.Process(target=getFriendsCount, args=(path,fb_dict ))
    p2 = multiprocessing.Process(target=getReceivedFriendRequestsCount, args=(path, fb_dict))
    p3 = multiprocessing.Process(target=getPageList, args=(path, fb_dict))
    p4 = multiprocessing.Process(target=getCommentsList, args=(path, fb_dict))
    p5 = multiprocessing.Process(target=getPostsInteractionsCount, args=(path, fb_dict))
    p6 = multiprocessing.Process(target=getImageSentimentInfo, args=(path, fb_dict))
    p7 = multiprocessing.Process(target=getProfileInfo, args=(path, fb_dict))
    p8 = multiprocessing.Process(target=getPostsList, args=(path, fb_dict))

    p1.start()
    p2.start()
    p3.start()
    p4.start()
    p5.start()
    p6.start()
    p7.start()
    p8.start()

    p1.join()
    p2.join()
    p3.join()
    p4.join()
    p5.join()
    p6.join()
    p7.join()
    p8.join()
    analysis_data['facebook_data']=fb_dict.copy()
    print(Fore.CYAN+"FACEBOOK DATA ANALYSIS COMPLETED")
    # totalFriends = getFriendsCount(path)
    # totalFriendRequestsRecieved =getReceivedFriendRequestsCount(path)
    # negativePageListPercentage = getPageList(path)
    # positiveComments,negativeComments, totalComments = getCommentsList(path)
    # totalReactionsOnPost = getPostsInteractionsCount(path) #Likes and Comments
    # totalNegativeImagesPercentage = getImageSentimentInfo(path)
    # profileInfo = getProfileInfo(path)
    # analysis_data['facebook']=fb_dict
