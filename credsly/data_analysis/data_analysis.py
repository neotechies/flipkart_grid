from credsly.data_analysis.scripts import linkedIn
import scripts
import multiprocessing
import pandas as pd
from datetime import datetime, date

def generate_credit_score(twitter_username, fb_zipname, linkedin_zipname, userID):
        manager = multiprocessing.Manager()
        analysis_data = manager.dict()
        p1 = multiprocessing.Process(target= scripts.getFacebookData, args=(fb_zipname,userID,analysis_data))
        p2 = multiprocessing.Process(target=scripts.getTwitterData, args=(twitter_username,analysis_data))
        p3 = multiprocessing.Process(target=scripts.getlinkedInData, args=(linkedin_zipname,userID,analysis_data))
        p1.start()
        p2.start()
        p3.start()

        p1.join()
        p2.join()
        p3.join()
        print(analysis_data)
        # print(json.dumps(analysis_data,sort_keys=False, indent=2))

generate_credit_score("mbcse50","asda","linkedin-mbcse50.zip","mohit1234")


def generate_sub_credit_score(analysis_data):
        
        data_table = pd.DataFrame(columns=['name', 'email', 'location','age','education','total_skills','total_connections','incoming_invitations','total_posts','total_likes','positive_posts_score','negative_posts_score','negative_image_score','comments_analysis_score','positive_page_score','negative_page_score','negative_groups'])
        full_name= analysis_data['linkedIn_data']['First Name']+" "+ analysis_data['linkedIn_data']['Last Name']
        
        #Fetching email row
        email=None
        if(analysis_data['linkedIn_data']['email']!=None):
                email=analysis_data['linkedIn_data']['email']
        elif(analysis_data['facebook_data']['profileInfo']['email']!=None):
                email=analysis_data['facebook_data']['profileInfo']['email']
                
        
        #Fetching location row
        location=None
        if(analysis_data['linkedIn_data']['profileJson']['Geo Location']!=None):
                location= analysis_data['linkedIn_data']['profileJson']['Geo Location']
        elif(analysis_data['twitter_data']['location']!=None):
                location= analysis_data['twitter_data']['location']
        
        #Fetching age row
        dob=None
        age=None
        if(analysis_data['facebook_data']['profileInfo']['dob']!=None):
                dob=analysis_data['facebook_data']['profileInfo']['dob']
        if(dob!=None):
                dob = datetime.strptime(dob, "%d/%m/%Y").date()
                today = date.today()
                age=today.year - dob.year - ((today.month,today.day) < (dob.month, dob.day))
                
        #Fetching the education row
        education_detail=None
        if(analysis_data['facebook_data']['profileInfo']['education_history']!=None):
                education_detail= analysis_data['facebook_data']['profileInfo']['education_history']
                
        #Fetching the total_skills row
        skills=None
        if(analysis_data['linkedIn_data']['skillsCount']!=None):
                skills= analysis_data['linkedIn_data']['skillsCount']
        
        #Fetching the total Connections
        fb_connections=0
        linkedIn_connections=0
        twitter_connections= 0
        
        if(analysis_data['linkedIn_data']['totalConnections']!=None):
                linkedIn_connections= analysis_data['linkedIn_data']['totalConnections']
                
        if(analysis_data['twitter_data']['followers']!=None):
                twitter_connections= analysis_data['twitter_data']['followers']
                
        if(analysis_data['c']['totalFriends']!=None):
                fb_connections= analysis_data['facebook_data']['totalFriends']
        total_connections= int((linkedIn_connections+twitter_connections+fb_connections)/3)     #Average of all three social media connections
        
        #Fetching incoming invitations row
        linkedIn_incoming=0
        fb_incoming=0
        if(analysis_data['linkedIn_data']['incomingInvitations']!=None):
                linkedIn_incoming=analysis_data['linkedIn_data']['incomingInvitations']
        if(analysis_data['facebook_data']['totalFriendRequestsRecieved']!=None):
                fb_incoming=analysis_data['facebook_data']['totalFriendRequestsRecieved']
        incoming_connections= int((linkedIn_incoming+fb_incoming)/2)                      #Average of LinkedIn and Facebook requests
        
        #Fetching total posts row
        fb_posts=0
        tweetNums=0
        if(analysis_data['twitter_data']['tweet_count']!=None):
                tweetNums= analysis_data['twitter_data']['tweet_count']
        if(analysis_data['facebook_data']['fb_posts']!=None):
                fb_posts= analysis_data['facebook_data']['fb_posts']
                
        
        total_posts= int((tweetNums+fb_posts)/2)
        
        # Getting total likes on posts
        twitter_likes=0
        fb_likes=0
        if(analysis_data['twitter_data']['total_likes']!=None):
                twitter_likes=analysis_data['twitter_data']['total_likes']
        if(analysis_data['facebook_data']['totalReactionsOnPost']!=None):
                fb_likes= analysis_data['facebook_data']['totalReactionsOnPost']
        total_likes= int((twitter_likes+fb_likes)/2)
        
        #fetching the positive post score
        twitter_positive=0
        if(analysis_data['twitter_data']['positivityScore']!=None):
                twitter_positive=analysis_data['twitter_data']['positivityScore']
        
        #Fetching the negative post score
        twitter_negative=0
        if(analysis_data['twitter_data']['positivityScore']!=None):
                twitter_negative=analysis_data['twitter_data']['negativityScore']
        
        # Fetching image analysis score
        negative_image_score=0
        if(analysis_data['facebook_data']['totalNegativeImagesPercentage']!=None):
                negative_image_score=analysis_data['facebook_data']['totalNegativeImagesPercentage']
                
        #Fetching the Positive comments score
        positive_comments=0
        negative_comments=0
        if(analysis_data['facebook_data']['positiveComments']!=None):
                positive_comments=analysis_data['facebook_data']['negativeComments']
        
        #Fetching the Negative comments score
        if(analysis_data['facebook_data']['negativeComments']!=None):
                negative_comments=analysis_data['facebook_data']['negativeComments']   
                
            
        
        
                
                
                
                
                
        
                
        
                
                 
                        
                        
                

                
        
        
        

                        
                
                
                
        
                
        