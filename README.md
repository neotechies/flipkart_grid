# CredSly: Social Credit Scoring System
`Trust and Affluence signal extraction from social media data`

`Flipkart_Grid 3.0`

## Requirements
- Python3 latest version recommended 
- pipenv(For virtual Environment) `Run pip3 install pipenv`

## How to Run Project
- Clone project and run `pipenv install`
- Run virtual environment `pipenv shell`
- To run webApp
  - `cd credsly`
  - `python3 manage.py runserver`
- To exit virtual environment run `exit`

## Problem Statement

Traditional and existing credit score assignments are basically used for determining the eligibility of a user to avail loan. The credit score is based on the  user’s financial status, transaction history, possessed assets, job etc. In short it analyses a user’s data from home to bank to analyze the fact whether the user will be able to repay the debt.
What it doesn’t check is the character and trust of other people on the user, user’s social engagement etc. Social media is one such tool where most of the people today shares day to day stuffs. This tool can be leveraged to determine some aspects of user’s life which the existing credit assignment companies doesn’t take into account. 
Social media provides a variety of data which gives us a peek into the user’s life and trust people have in user. User’s day to day posts, followers, likes, dislikes, daily interactions and more such stuff gives ample data to assess other factors besides financial history.
Flipkart has introduced some amazing offers and features for its users like:
Flipkart Pay Later
Avail EMI
These features can use this new innovative method of credit score assignment based on social media to give more benefits to the trustworthy users. Besides  more discount for trustworthy users and more such things can be introduced to attract more users. 

## Flow Diagram
![](https://github.com/neotechies/flipkart_grid/blob/main/assets/Flipkart%20GRID.png)

## Data Extraction and Pre-processing
The dataset in this project has been sourced from three major social medias:
Twitter
Facebook
LinkedIn
The twitter data is easily accessible from the twitter’s developer account via ‘tweepy’ python package. But Facebook and LinkedIn doesn’t provide permission to other users easily to use someone else’s data. But one can always get their own data if requested to these social media support team. So, a user can bring their own data from Facebook and LinkedIn (which is provided in the form of zip file) and upload on the portal. For the Twitter, one just needs to enter the username of the twitter handle and all the necessary data will be fetched for the further analysis.

All the data from the three social media sources have been pre-processed and organized in the json format for the analysis of various credit features. 
Various useful details have been extracted from LinkedIn like- 
- Profile Information: Name, Location, Email, Industry, DOB
- Total Connections
- Invitations received
- Skills

From twitter, we extracted the following features for the analysis:

- Followers
- Tweet Count
- Bio
- Twitter age
- Likes on tweets
- Likes
- All the tweets by the user

Similarly, from facebook following many features have been captured for processing:

- FollowersProfile Information: Name, DOB, Education History
- Total Friends
- Groups in which user is present
- Total posts by the user
- Total images posted by the user
- Total comments by the user and its analysis
- Likes and reactions by the user on pages and other posts

All these above features that have been taken out of the data from the social media have been classified into the different features required for determining credit score.

![](https://github.com/neotechies/flipkart_grid/blob/main/assets/json.png)

## Technical Approach 
All the features that have been extracted from all the social medias have been characterized into the following features:
- Age 
- Educational details
- Positivity analysis of posts and tweets
- Negativity Analysis of posts and tweets
- Analysis of the names of groups user is present in
- Analysis of users day to day interaction (comments and replies)
- Analysis of pages user has liked
- Interaction frequency of users
- Image Analysis of user’s post
- Followers, connections and Friends
- Skills Analysis

![](https://github.com/neotechies/flipkart_grid/blob/main/assets/pd1.png)

For the content analysis of the user’s posts, sentiment analysis model is implemented to  calculate the overall positivity and negativity on the posts. All these sentiment will contribute to increasing or decreasing the credit score of the user. 

![](https://github.com/neotechies/flipkart_grid/blob/main/assets/sentiment.png)

![](https://github.com/neotechies/flipkart_grid/blob/main/assets/pd2.png)

Deep learning powered Image recognition model is used to detect the nudity,violence and obnoxious stuffs in the image posted by the users. This factor will further decrement a users credit score.

![](https://github.com/neotechies/flipkart_grid/blob/main/assets/imageanalysis.png)

Also NLP based python package is used to analyze the profanity of the groups user has joined and the kind of pages user has liked. If the NLP model detects that the user is in wrong groups and has liked repugnant pages, this will put a question mark on the trust issues of the users and will decrement the credit score.

All these models were kind of making our whole algorithm slow and time consuming. In order to tackle that we have used parallel processing at the functional and non-functional level both which has reduced the time consumption significantly. We are using multiprocessing to run our functions at different processors at the same time.

![](https://github.com/neotechies/flipkart_grid/blob/main/assets/multiprocessing1.png)

## Credit Score Generation Algorithm

#### We have kept three levels of priority order- 
- Priority one score
- Priority two score
- Priority three score

![](https://github.com/neotechies/flipkart_grid/blob/main/assets/prioirtyscores.png)

#### The Calculations
- Different features have been assigned different priorities based on the priorities and their magnitude of contribution.
In case of age, if a user is below 18, the user is announced ineligible for determining credit worthiness. The user’s credit worthiness increases linearly  from the age of 18 and reaches its peak at 35 from where it again starts decreasing. After the age of 65, the user again becomes ineligible for any credit score. The following graph and it’s equation aptly captures the credit score assignment based on age factor:

- In case of total connections, followers and friends from all these social medias, we are taking the average of all these to combine it into one feature. Then we are taking a threshold number(80k) of followers below which the credit score is increasing gradually. After that threshold value, every user gets the same priority score. Basically the more number of followers emphasizes the fact that more people trust him and thus credit score can be increased. 

- Similar graph pattern is followed for the skills feature to assign the credit score.

- Some features like “total likes on user’s post”, “positive posts” and “positive comments” follow a linear pattern i.e. more the number of likes on the post, more the credit score.

- Similarly there are some negative features like “negative groups user has joined”, “negative pages user has liked” which will reduce the credit score of the user following the negative linear pattern i.e. more the negatives groups user has joined, more the credit loss user will have.

**Best part is you can modify the weightage of priority scores from the admin panel of the website as per your convenience, this will change the credit score and total credit accordingly**.

![](https://github.com/neotechies/flipkart_grid/blob/main/assets/Screenshot%20from%202021-09-30%2022-39-08.png)

## Tech Stack
- Django
- Machine Learning
- NLP
- AWS cloud
- Python
- HTML/CSS/JAVASCRIPT
- Bootstrap5

## Result/Output
![](https://github.com/neotechies/flipkart_grid/blob/main/assets/outputconsole.png)

![](https://github.com/neotechies/flipkart_grid/blob/main/assets/credit_output.png)

![](https://github.com/neotechies/flipkart_grid/blob/main/assets/dashboard.png)
## Project Demo
Github : [https://github.com/neotechies/flipkart_grid](https://github.com/neotechies/flipkart_grid)

Youtube link: [https://youtu.be/XkjB2aOOajs](https://youtu.be/XkjB2aOOajs)

## Challenges Faced

- Despite all the attempts, we couldn’t get the facebook and linkedIn data from their API as they don’t provide access for it, we had to resort to the user uploading  his data after downloading it from their account settings.
- It was challenging to process the .zip data of facebook and linkedIn as it contains subfolders with all the data present in an unstructured way.
- It was tough to optimise the time taken by the heavy machine learning and deep learning based models. 

## Future Scopes

- We will also add analysis of Instagram data 
- We will make setting of priorities of extracted features possible from admin panel
- We will try to further reduce the time taken  for credit score generation
- We will make the whole system as configurable as possible so that companies like flipkart can modify it according to their needs.

# Team
- MOHIT BHAT (mbcse50@gmail.com)
- AVINASH KUMAR (avinashrkmv@gmail.com)

