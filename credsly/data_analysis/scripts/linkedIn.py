from zipfile import ZipFile
import os
import shutil
import json
import pandas as pd
import boto3
import base64
import multiprocessing
from pathlib import Path
import colorama
from colorama import Fore

###################################################Configurations#########################################################################################################################
ACCESS_KEY="AKIAQI6GMTIGYNVJZOAQ"
SECRET_KEY="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"

BASE_DIR = Path(__file__).resolve().parent.parent.parent

#####################################################AWS Clients################################################################################################################

client = boto3.client(
    'comprehend',
    aws_access_key_id=ACCESS_KEY,
    aws_secret_access_key=SECRET_KEY,
    region_name = 'us-west-2'
)

######################################For Testing#####################################################################################################################################

# file_name = "../userDataUploads/linkedInData.zip"  #testing
# userID='avinash'
# path="../userDataUploads/"+userID+"/linkedIn" #testing

########################################Checking and making directory for zip Extraction####################################################################################################################
def checkAndMakeDir(userID):
    if(os.path.isdir(str(BASE_DIR)+"/userDataUploads/"+userID)):
        if(os.path.isdir(str(BASE_DIR)+"/userDataUploads/"+userID+"/linkedIn")):
            shutil.rmtree(str(BASE_DIR)+"/userDataUploads/"+userID+"/linkedIn")
            os.mkdir(str(BASE_DIR)+"/userDataUploads/"+userID+"/linkedIn") 
        else:
            os.mkdir(str(BASE_DIR)+"/userDataUploads/"+userID+"/linkedIn")   
    else:
        os.makedirs(str(BASE_DIR)+"/userDataUploads/"+userID+"/linkedIn")
        
        
#***************************************Fetching profile information**********************************************************************************************************************

def getProfileInfo(path,linkedIn_dict):
    print(Fore.GREEN +"Starting the Linkedin Profile Info analysis...")
    
    try:
        filePath=path+'/Profile.csv'
        data=pd.read_csv(filePath,error_bad_lines=False)
        profileJson=data.to_json(orient = 'records')[1:-1].replace('},{', '} {')
        linkedIn_dict['profileJson']=json.loads(profileJson)
        # return profileJson
            
    except Exception as e:
        print(Fore.RED +str(e))
        linkedIn_dict['profileJson']=None
        # return None
    finally:
        print(Fore.YELLOW +"Linkedin Profile Info Analysis completed!!")
        
    
#profileJson=getProfileInfo(path)

#************************************************************************************************************************************************************

def getEmail(path,linkedIn_dict):
    print(Fore.GREEN +"Fetching the user's email...")
    try:
        filePath=path+'/Email Addresses.csv'
        data=pd.read_csv(filePath,error_bad_lines=False)
        emailJson=data.to_json(orient = 'records')[1:-1].replace('},{', '} {')
        linkedIn_dict['email']=json.loads(emailJson)["Email Address"]
        # return emailJson
    except Exception as e:
        print(Fore.RED + str(e))
        linkedIn_dict['email']=None
        # return None
    finally:
        print(Fore.YELLOW +"User Email fetched!!!")
    
#************************************************************************************************************************************************

def getSentInvitations(path,linkedIn_dict):
    print(Fore.GREEN +"Analysing the Incoming Invitations...")
    try:
        filePath=path+'/Invitations.csv'
        data=pd.read_csv(filePath,error_bad_lines=False)
        filtered_data= data[data['Direction'] =='INCOMING']
        sentInvitations=len(filtered_data)
        linkedIn_dict['incomingInvitations']=sentInvitations
        # return sentInvitations
        
    except Exception as e:
        print(Fore.RED +str(e))
        linkedIn_dict['incomingInvitations']=None
        # return None
    
    finally:
        print(Fore.YELLOW +'Incoming Invitations Analysis completed!!!')

#********************************************************************************************************************************************

def getSkills(path,linkedIn_dict):
    print(Fore.GREEN +"Extracting the Users Skills...")
    try:
        filePath=path+'/Skills.csv'
        data=pd.read_csv(filePath,error_bad_lines=False)
        skillsCount= len(data)
        linkedIn_dict['skillsCount']=skillsCount
        # return skillsCount
        
    except Exception as e:
        print(Fore.RED +str(e))
        linkedIn_dict['skillsCount']=None
        # return None
    
    finally:
        print(Fore.YELLOW +"User Skills Extraction Completed!!!")

#................................................................................................................................................................................#

def getTotalConnections(path,linkedIn_dict):
    print(Fore.GREEN +"Analysing the LinkedIn Connections...")
    try:
        filePath=path+'/Connections.csv'
        data=pd.read_csv(filePath,error_bad_lines=False,skiprows=3)
        totalConnections=len(data)
        linkedIn_dict['totalConnections']=totalConnections
        # return totalConnections
    except Exception as e:
        print(Fore.RED +str(e))
        linkedIn_dict['totalConnections']=None   
    
    finally:
        print(Fore.YELLOW +"LinkedIn Connections Analysis Completed!!!")
            
#................................................................................................................................................................................#

def getlinkedInData(zipName,userID,analysis_data):
    print(Fore.GREEN +"STARTING LINKEDIN DATA ANALYSIS")

    checkAndMakeDir(userID)
    path=str(BASE_DIR)+"/userDataUploads/"+userID+"/linkedIn"
    filename = str(BASE_DIR)+"/userDataUploads/ZIP_UPLOADS/"+zipName
    with ZipFile(filename, 'r') as zip:
        # extracting all the files
        zip.extractall(path)
    
    manager = multiprocessing.Manager()
    linkedIn_dict = manager.dict()
    p1 = multiprocessing.Process(target=getProfileInfo, args=(path,linkedIn_dict ))
    p2 = multiprocessing.Process(target=getEmail, args=(path, linkedIn_dict))
    p3 = multiprocessing.Process(target=getSentInvitations, args=(path, linkedIn_dict))
    p4 = multiprocessing.Process(target=getSkills, args=(path, linkedIn_dict))
    p5 = multiprocessing.Process(target=getTotalConnections, args=(path, linkedIn_dict))

    p1.start()
    p2.start()
    p3.start()
    p4.start()
    p5.start()

    p1.join()
    p2.join()
    p3.join()
    p4.join()
    p5.join()
      
    analysis_data['linkedIn_data']=linkedIn_dict.copy()
    print(Fore.CYAN +"LINKEDIN DATA ANALYSIS COMPLETED")

    # linkedInData={}
    
    # profileJson=getProfileInfo(path) 
    # email=getEmail(path)
    # sentInvites=getSentInvitations(path)
    # skillsCount=getSkills(path)
    # totalConnections=getTotalConnections(path)
    
    # linkedInData['profileData']=profileJson
    # linkedInData['email']= email
    # linkedInData['incomingConnections']=sentInvites
    # linkedInData['skills']=skillsCount
    # linkedInData['totalConnections']= totalConnections
    
    
# if __name__ == '__main__':
#     linkedInData=getlinkedInData(file_name,'aaaa')
#     print(Fore.GREEN +linkedInData)

#................................................................................................................................................................................#
