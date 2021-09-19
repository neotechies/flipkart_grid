from zipfile import ZipFile
import os
import shutil
import json
import pandas as pd
import boto3
import base64

ACCESS_KEY="AKIAQI6GMTIGYNVJZOAQ"
SECRET_KEY="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"
# client = boto3.client(
#     'rekognition',
#     aws_access_key_id=ACCESS_KEY,
#     aws_secret_access_key=SECRET_KEY,
#     region_name = 'us-west-2'
# )

client = boto3.client(
    'comprehend',
    aws_access_key_id=ACCESS_KEY,
    aws_secret_access_key=SECRET_KEY,
    region_name = 'us-west-2'
)


file_name = "../userDataUploads/linkedInData.zip"  #testing
userID='avinash'
path="../userDataUploads/"+userID+"/linkedIn" #testing

def checkAndMakeDir(userID):
    if(os.path.isdir("../userDataUploads/"+userID)):
        if(os.path.isdir("../userDataUploads/"+userID+"/linkedIn")):
            shutil.rmtree("../userDataUploads/"+userID+"/linkedIn")
            os.mkdir("../userDataUploads/"+userID+"/linkedIn") 
        else:
            os.mkdir("../userDataUploads/"+userID+"/linkedIn")   
    else:
        os.makedirs("../userDataUploads/"+userID+"/linkedIn")
        
        

# Fetching profile information
def getProfileInfo(path):
    
    try:
        filePath=path+'/Profile.csv'
        data=pd.read_csv(filePath,error_bad_lines=False)
        profileJson=data.to_json(orient = 'records')[1:-1].replace('},{', '} {')
        return profileJson
            
    except Exception as e:
        print(e)
        return None
#profileJson=getProfileInfo(path)


def getEmail(path):
    try:
        filePath=path+'/Email Addresses.csv'
        data=pd.read_csv(filePath,error_bad_lines=False)
        emailJson=data.to_json(orient = 'records')[1:-1].replace('},{', '} {')
        return emailJson
    except Exception as e:
        print(e)
        return None
    
#email=getEmail(path)

def getSentInvitations(path):
    try:
        filePath=path+'/Invitations.csv'
        data=pd.read_csv(filePath,error_bad_lines=False)
        filtered_data= data[data['Direction'] =='INCOMING']
        sentInvitations=len(filtered_data)
        return sentInvitations
        
    except Exception as e:
        print(e)
        return None
# sentInvites=getSentInvitations(path)
# print(sentInvites)

def getSkills(path):
    try:
        filePath=path+'/Skills.csv'
        data=pd.read_csv(filePath,error_bad_lines=False)
        skillsCount= len(data)
        return skillsCount
        
    except Exception as e:
        print(e)
        return None
#skillscount=getSkills(path)

def getTotalConnections(path):
    try:
        filePath=path+'/Connections.csv'
        data=pd.read_csv(filePath,error_bad_lines=False,skiprows=3)
        totalConnections=len(data)
        return totalConnections
    except Exception as e:
        print(e)
        return None   
        
# totalConnections=getTotalConnections(path)
# print(totalConnections)
        
        
        



# def getlinkedInData(zipName, userID):
#     checkAndMakeDir(userID)
#     path="../userDataUploads/"+userID+"/linkedIn"

#     with ZipFile(file_name, 'r') as zip:
#         # extracting all the files
        
#         zip.extractall(path)
    
    
    
#getlinkedInData(file_name,'avinash')


image = open(path+"/cat.jpg", 'rb')

image_read = image.read()


response = client.detect_moderation_labels(
    Image={
        'Bytes': image_read,
    }
)


print(response)