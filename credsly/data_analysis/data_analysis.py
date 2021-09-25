import scripts
import multiprocessing

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
        return

generate_credit_score("mbcse50","asda","linkedin-mbcse50.zip","mohit1234")