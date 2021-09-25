from zipfile import ZipFile
import os
import shutil
import json
import pandas as pd
import boto3
import base64
import multiprocessing

#................................................................................................................................................................................#
#AWS client credentials

ACCESS_KEY="AKIAQI6GMTIGYNVJZOAQ"
SECRET_KEY="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"


client = boto3.client(
    'comprehend',
    aws_access_key_id=ACCESS_KEY,
    aws_secret_access_key=SECRET_KEY,
    region_name = 'us-west-2'
)

#................................................................................................................................................................................#


# file_name = "../userDataUploads/linkedInData.zip"  #testing
# userID='avinash'
# path="../userDataUploads/"+userID+"/linkedIn" #testing

#................................................................................................................................................................................#
def checkAndMakeDir(userID):
    if(os.path.isdir("../userDataUploads/"+userID)):
        if(os.path.isdir("../userDataUploads/"+userID+"/linkedIn")):
            shutil.rmtree("../userDataUploads/"+userID+"/linkedIn")
            os.mkdir("../userDataUploads/"+userID+"/linkedIn") 
        else:
            os.mkdir("../userDataUploads/"+userID+"/linkedIn")   
    else:
        os.makedirs("../userDataUploads/"+userID+"/linkedIn")
        
        
#................................................................................................................................................................................#

# Fetching profile information
def getProfileInfo(path,linkedIn_dict):
    print("Starting the profile Info analysis...")
    
    try:
        filePath=path+'/Profile.csv'
        data=pd.read_csv(filePath,error_bad_lines=False)
        profileJson=data.to_json(orient = 'records')[1:-1].replace('},{', '} {')
        linkedIn_dict['profileJson']=json.loads(profileJson)
        # return profileJson
            
    except Exception as e:
        print(e)
        linkedIn_dict['profileJson']=None
        # return None
    finally:
        print("Analysis completed!!")
        
    
#profileJson=getProfileInfo(path)

#................................................................................................................................................................................#

def getEmail(path,linkedIn_dict):
    print("Fetching the user's email...")
    try:
        filePath=path+'/Email Addresses.csv'
        data=pd.read_csv(filePath,error_bad_lines=False)
        emailJson=data.to_json(orient = 'records')[1:-1].replace('},{', '} {')
        linkedIn_dict['email']=json.loads(emailJson)["Email Address"]
        # return emailJson
    except Exception as e:
        print(e)
        linkedIn_dict['email']=None
        # return None
    finally:
        print("email fetched!!!")
    
#email=getEmail(path)

#................................................................................................................................................................................#


def getSentInvitations(path,linkedIn_dict):
    print("Analysisng the incoming invitations...")
    try:
        filePath=path+'/Invitations.csv'
        data=pd.read_csv(filePath,error_bad_lines=False)
        filtered_data= data[data['Direction'] =='INCOMING']
        sentInvitations=len(filtered_data)
        linkedIn_dict['incomingInvitations']=sentInvitations
        # return sentInvitations
        
    except Exception as e:
        print(e)
        linkedIn_dict['incomingInvitations']=None
        # return None
    
    finally:
        print('Analysis completed!!!')

#................................................................................................................................................................................#

        
# sentInvites=getSentInvitations(path)
# print(sentInvites)

def getSkills(path,linkedIn_dict):
    print("Extracting the users skills...")
    try:
        filePath=path+'/Skills.csv'
        data=pd.read_csv(filePath,error_bad_lines=False)
        skillsCount= len(data)
        linkedIn_dict['skillsCount']=skillsCount
        # return skillsCount
        
    except Exception as e:
        print(e)
        linkedIn_dict['skillsCount']=None
        # return None
    
    finally:
        print("Extraction done!!!")
#skillscount=getSkills(path)

#................................................................................................................................................................................#

def getTotalConnections(path,linkedIn_dict):
    print("Analysing the total linkedIn connections...")
    try:
        filePath=path+'/Connections.csv'
        data=pd.read_csv(filePath,error_bad_lines=False,skiprows=3)
        totalConnections=len(data)
        linkedIn_dict['totalConnections']=totalConnections
        # return totalConnections
    except Exception as e:
        print(e)
        linkedIn_dict['totalConnections']=None   
    
    finally:
        print("Analysis done!!!")
        
# totalConnections=getTotalConnections(path)
# print(totalConnections)
   
   
        
#................................................................................................................................................................................#

        

def getlinkedInData(zipName,userID,analysis_data):
    checkAndMakeDir(userID)
    path="../userDataUploads/"+userID+"/linkedIn"

    with ZipFile(zipName, 'r') as zip:
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
#     linkedInData=getlinkedInData(file_name,'avinash')
#     print(linkedInData)

analysis_data={}
linkedInData=getlinkedInData("../userDataUploads/linkedin-mbcse50.zip",'mohit1234',analysis_data )
print(analysis_data)


#................................................................................................................................................................................#
