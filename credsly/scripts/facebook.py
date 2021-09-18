from zipfile import ZipFile
import os
import shutil
import json

file_name = "../userDataUploads/fbdata.zip"  #testing



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
    
    with ZipFile(file_name, 'r') as zip:
        # extracting all the files
        path="../userDataUploads/"+userID+"/facebook"
        zip.extractall(path)


def friendsCount(userID):
    try:
        
    except Exception as e:
        print("Error while Getting Friends Count for Facebook")


