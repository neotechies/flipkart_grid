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
        #print(analysis_data)
        # print(json.dumps(analysis_data,sort_keys=False, indent=2))
        data_table=generate_table(analysis_data)
        table_form=pd.DataFrame(data_table)
        
        
        

generate_credit_score("mbcse50","asda","linkedin-mbcse50.zip","mohit1234")




def generate_table(analysis_data):
        
        data_table = pd.DataFrame(columns=['name', 'email', 'location','age','education',
                                           'total_skills','total_connections','incoming_invitations',
                                           'total_posts','total_likes','positive_posts_score','negative_posts_score',
                                           'negative_image_score','positive_comments_score','negative_comments_score','negative_page_score',
                                           'negative_groups','social_interaction'])
        full_name= analysis_data['linkedIn_data']['profileJson']['First Name']+" "+ analysis_data['linkedIn_data']['profileJson']['Last Name']
        
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
                
        if(analysis_data['facebook_data']['totalFriends']!=None):
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
        if(analysis_data['facebook_data']['totalPosts']!=None):
                fb_posts= analysis_data['facebook_data']['totalPosts']
                
        
        total_posts= int((tweetNums+fb_posts)/2)
        
        # Getting total likes on posts
        twitter_likes=0
        
        if(analysis_data['twitter_data']['total_likes']!=None):
                twitter_likes=analysis_data['twitter_data']['total_likes']
        
        total_likes= twitter_likes
        
        #Fetching facebook reactions on posts
        fb_likes=0
        fb_comments=0
        fb_timestamp=None
        if(analysis_data['facebook_data']['totalReactionsOnPost']!=None):
                fb_likes= analysis_data['facebook_data']['totalReactionsOnPost']
        if(analysis_data['facebook_data']['totalComments']!=None):
                fb_comments= analysis_data['facebook_data']['totalComments']
        if(analysis_data['facebook_data']['fb_registration']!=None):
                fb_timestamp= analysis_data['facebook_data']['fb_registration']
        today= datetime.now()
        joining_date=datetime.fromtimestamp(int(fb_timestamp))
        interaction_days=today-joining_date
        
        fb_interaction=(fb_comments+fb_likes+fb_posts)/(interaction_days.days)
        
        #fetching the positive post score
        twitter_positive=0
        fb_positive=0
        if(analysis_data['twitter_data']['positivityScore']!=None):
                twitter_positive=analysis_data['twitter_data']['positivityScore']
        if(analysis_data['facebook_data']['positivePosts']!=None):
                fb_positive= analysis_data['facebook_data']['positivePosts']
        post_positive=(twitter_positive+fb_positive)/2
        
        #Fetching the negative post score
        twitter_negative=0
        fb_negative=0
        if(analysis_data['twitter_data']['positivityScore']!=None):
                twitter_negative=analysis_data['twitter_data']['negativityScore']
        if(analysis_data['facebook_data']['negativePosts']!=None):
                fb_negative= analysis_data['facebook_data']['negativePosts']
        post_negative=(twitter_positive+fb_negative)/2
        
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
        
        #Fetching the negative group score
        negative_group=0  
        if(analysis_data['facebook_data']['profileInfo']['negativeGroupPercentage']!=None):
                negative_group= analysis_data['facebook_data']['profileInfo']['negativeGroupPercentage']
        
        #Fetching the negative groups
        negative_page=0
        if(analysis_data['facebook_data']['negativePageListPercentage']!=None):
                negative_page=analysis_data['facebook_data']['negativePageListPercentage']
                
        
        
        data_table = data_table.append({'name':full_name, 'email':email, 'location':location,'age':age,'education':education_detail,
                                           'total_skills':skills,'total_connections':total_connections,'incoming_invitations':incoming_connections,
                                           'total_posts':total_posts,'total_likes':total_likes,'positive_posts_score':post_positive,'negative_posts_score':post_negative,
                                           'negative_image_score':negative_image_score,'positive_comments_score':positive_comments,'negative_comments_score':negative_comments,'negative_page_score':negative_page,
                                           'negative_groups':negative_group,'social_interaction':fb_interaction}, ignore_index=True)
                
                
        
        return data_table


data_table=generate_table(analysis_data)
table_form=pd.DataFrame(data_table)
     
                
                
            
def credit_assignment(x):   #pass table_form as argument

    credit_score=0
    priority_one_score=100
    priority_two_score=80
    priority_three_score=50
    if(x['age'][0]>18 and x['age'][0]<=35):
        credit_score+= x['age'][0]*2.857
    elif(x['age'][0]>35 and x['age'][0]<65):
        credit_score+= priority_one_score-(x['age'][0]/(65-x['age'][0]))
    elif(x['age'][0]<18):
        print("Not eligible due to age")


    if(x['total_connections'][0]>=80000):
        credit_score+=priority_one_score
    elif((x['total_connections'][0]<80000)):
        credit_score+= (priority_one_score/80000)*x['total_connections']

    if(x['total_skills'][0]>25):
        credit_score+= priority_three_score
    elif(x['total_skills'][0]<=25 and x['total_skills']>=1):
        credit_score+=priority_three_score- (x['total_skills'][0]/(25-x['total_skills'][0]))

    invitationPercent=(x['incoming_invitations'][0]/x['total_connections'][0])
    credit_score+= (invitationPercent*priority_three_score)

    likePercent= (x['total_likes'][0]/x['total_posts'][0])
    credit_score+= (likePercent*priority_three_score)

    credit_score+= x['positive_posts_score'][0]
    credit_score-= x['negative_posts_score'][0]

    credit_score+= priority_one_score-(x['negative_image_score'][0]*priority_one_score)

    credit_score+= x['positive_comments_score'][0]
    credit_score-= x['negative_comments_score'][0]


    credit_score+= priority_two_score-(x['negative_image_score'][0]*priority_two_score)

    credit_score+= priority_two_score-(x['negative_groups'][0]*priority_two_score)

    return credit_score
     

                
                 
                        
                        
                

                
        
        
        

                        
                
                
                
        
                
        