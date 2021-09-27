from data_analysis import scripts
import multiprocessing
import pandas as pd
from datetime import datetime, date

def generate_table(analysis_data):
        
        data_table = pd.DataFrame(columns=['name', 'email', 'location','age','education',
                                           'total_skills','total_connections','incoming_invitations',
                                           'total_posts','total_likes','positive_posts_score','negative_posts_score',
                                           'negative_image_score','positive_comments_score','negative_comments_score','negative_page_score',
                                           'negative_groups','social_interaction'])

        #Fetching Full Name                                   
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
                age = today.year - dob.year - ((today.month,today.day) < (dob.month, dob.day))
                
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

        #Average of all three social media connections        
        total_connections= int((linkedIn_connections+twitter_connections+fb_connections)/3)     
        
        #Fetching incoming invitations row
        linkedIn_incoming=0
        fb_incoming=0
        if(analysis_data['linkedIn_data']['incomingInvitations']!=None):
                linkedIn_incoming=analysis_data['linkedIn_data']['incomingInvitations']
        if(analysis_data['facebook_data']['totalFriendRequestsRecieved']!=None):
                fb_incoming=analysis_data['facebook_data']['totalFriendRequestsRecieved']

        #Average of LinkedIn and Facebook requests        
        incoming_connections= int((linkedIn_incoming+fb_incoming)/2)                      
        
        #Fetching total posts row
        fb_posts=0
        tweetNums=0
        if(analysis_data['twitter_data']['tweet_count']!=None):
                tweetNums= analysis_data['twitter_data']['tweet_count']
        if(analysis_data['facebook_data']['totalPosts']!=None):
                fb_posts= analysis_data['facebook_data']['totalPosts']
                
        #Average of Tiwtter and Facebook Posts
        total_posts= int((tweetNums+fb_posts)/2)
        
        # Getting total likes on posts
        total_likes = 0
        twitter_likes=0
        if(analysis_data['twitter_data']['total_likes']!=None):
                twitter_likes=analysis_data['twitter_data']['total_likes']
        
        total_likes= twitter_likes
        
        #Fetching facebook reactions on posts
        fb_likes=0
        fb_comments=0
        
        if(analysis_data['facebook_data']['totalReactionsOnPost']!=None):
                fb_likes= analysis_data['facebook_data']['totalReactionsOnPost']
        if(analysis_data['facebook_data']['totalComments']!=None):
                fb_comments= analysis_data['facebook_data']['totalComments']
        
        #Fetching No of days since joined social Medias
        interaction_days = 0.001 # least For Division Purpose
        fb_timestamp=None  
              
        if(analysis_data['facebook_data']['profileInfo']['fb_registration']!=None):
                fb_timestamp= analysis_data['facebook_data']['profileInfo']['fb_registration']

        today= datetime.now()
        fb_joining_date=datetime.fromtimestamp(int(fb_timestamp))

        interaction_days=today-fb_joining_date
        
        #Taking All types of interactions sum posts,likes and comments and calculating Frequency by using no of days since joined
        fb_interaction=(fb_comments+fb_likes+fb_posts)/(interaction_days.days)
        
        #Fetching the positive post score
        twitter_positive_posts=0
        fb_positive_posts=0
        if(analysis_data['twitter_data']['positivityScore']!=None):
                twitter_positive_posts=analysis_data['twitter_data']['positivityScore']
        if(analysis_data['facebook_data']['positivePosts']!=None):
                fb_positive_posts= analysis_data['facebook_data']['positivePosts']

        post_positive=(twitter_positive_posts+fb_positive_posts)/2
        
        #Fetching the negative post score
        twitter_negative_posts=0
        fb_negative_posts=0
        if(analysis_data['twitter_data']['negativityScore']!=None):
                twitter_negative_posts=analysis_data['twitter_data']['negativityScore']
        if(analysis_data['facebook_data']['negativePosts']!=None):
                fb_negative_posts= analysis_data['facebook_data']['negativePosts']

        post_negative=(twitter_negative_posts+fb_negative_posts)/2
        
        # Fetching image analysis score
        negative_image_score=0
        if(analysis_data['facebook_data']['totalNegativeImagesPercentage']!=None):
                negative_image_score=analysis_data['facebook_data']['totalNegativeImagesPercentage']
                
        #Fetching the Positive comments score
        positive_comments=0
        negative_comments=0
        if(analysis_data['facebook_data']['positiveComments']!=None):
                positive_comments=analysis_data['facebook_data']['positiveComments']/fb_comments
        
        #Fetching the Negative comments score
        if(analysis_data['facebook_data']['negativeComments']!=None):
                negative_comments=analysis_data['facebook_data']['negativeComments']/fb_comments   
        
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
                        
        return data_table,total_posts,total_likes,fb_comments,total_connections          
            
def credit_assignment(data_table):
    credit_score=0
    total_credit=0

    priority_one_score=100
    priority_two_score=80
    priority_three_score=50

    priority_map={
            'age': priority_one_score,
            'total_connections': priority_one_score,
            'positive_posts_score': priority_one_score,
            'negative_posts_score': priority_one_score,
            'negative_image_score': priority_one_score,

            'negative_page_score':priority_two_score,
            'positive_comments_score': priority_two_score,
            'negative_comments_score':priority_two_score,
            'negative_groups' : priority_two_score,

            'total_skills': priority_three_score,
            'incoming_invitations': priority_three_score,
            'total_likes': priority_three_score,
    }

    dont_count=['negative_comments_score','negative_posts_score']
    
    print(credit_score)

    # Calculating Total Credit score
    for key in priority_map:
            if key not in dont_count:
                total_credit+=priority_map[key]

    # Getting Score For age Min age 18 and max age 65
    # Max Credit Score Age 35
    multiplier = priority_map['age']/35
    if(data_table['age'][0]>=18 and data_table['age'][0]<=35):
        credit_score+= data_table['age'][0]*multiplier
    elif(data_table['age'][0]>35 and data_table['age'][0]<65):
        credit_score+= priority_map['age']-(data_table['age'][0]/(65-data_table['age'][0]))
    elif(data_table['age'][0]<18):
        print("Not eligible due to age")

    print(credit_score)     

    # Generating Credit Score From Total Connections
    if(data_table['total_connections'][0]>=80000):
        credit_score+=priority_map['total_connections']
    elif((data_table['total_connections'][0]<80000)):
        credit_score+= ((priority_map['total_connections']/80000)*data_table['total_connections'][0])

    print(credit_score) 

    # Generating Credit Score From Total Skills 
    skill_count=data_table['total_skills'][0]
    if(skill_count>25):
        credit_score+= priority_map['total_skills']
    elif(skill_count<=25 and skill_count>=1):
        credit_score+=(priority_map['total_skills']/25)*skill_count

    print(credit_score)    

    # Generating credit Score from Invitations
    invitationPercent=(data_table['incoming_invitations'][0]/data_table['total_connections'][0])
    credit_score+= (invitationPercent*priority_map['incoming_invitations'])

    print(credit_score)

    # Generating credit Score from Likes
    likePercent= (data_table['total_likes'][0]/data_table['total_posts'][0])
    credit_score+= (likePercent*priority_map['total_likes'])

    print(credit_score)

    # Generating credit Score from Positive Posts
    credit_score+= (data_table['positive_posts_score'][0]*priority_map['positive_posts_score'])
    
    print(credit_score)

    # Generating credit Score from Negative Posts    
    credit_score-= (data_table['negative_posts_score'][0]*priority_map['negative_posts_score'])
    
    print(credit_score)

    # Generating credit Score from Negative Images   
    credit_score+= (priority_map['negative_image_score']-(data_table['negative_image_score'][0]*priority_map['negative_image_score']))
    
    print(credit_score)

    # Generating credit Score from Negative pages   
    credit_score+= (priority_map['negative_page_score']-(data_table['negative_page_score'][0]*priority_map['negative_page_score']))

    print(credit_score)

    # Generating credit Score from Postive Comments   
    credit_score+= (data_table['positive_comments_score'][0]*priority_map['positive_comments_score'])
    
    print(credit_score)

    # Generating credit Score from Negative Comments   
    credit_score-=(data_table['negative_comments_score'][0]*priority_map['negative_comments_score'])

    print(credit_score)

    # Generating credit Score from Negative Groups  
    credit_score+= (priority_map['negative_groups']-(data_table['negative_groups'][0]*priority_map['negative_groups']))
    
    print(credit_score)

    # Returning Credit Score and total Credit
    return credit_score,total_credit

     

def generate_credit_score(userID, twitter_username, fb_zipname, linkedin_zipname):
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

        try:
                data_table,total_posts,total_likes,fb_comments,total_connections=generate_table(analysis_data)
                table_form=pd.DataFrame(data_table)
                credit_score,total_credit= credit_assignment(table_form)
                print(credit_score,total_credit)
                return credit_score,total_credit,total_posts,total_likes,fb_comments,total_connections
        except Exception as e:
                print(e)
                return None,None,None,None,None,None
                
                 
                        
                        
                

                
        
        
        

                        
                
                
                
        
                
        