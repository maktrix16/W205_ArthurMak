import sys
import os
import json
import pymongo
import datetime

tweets_mongo = [] #this is the variable for storing the format needed for inserting into MongoDB
hashtags_temp = []

for filename in os.listdir("."):  #loop through each file in current directory
	if filename.endswith(".json"): #only interact with those with specific extension
		f = open(filename.strip(),"r")
		tweets_raw = json.load(f)

		#extract only the needed info looping through each tweet data
		for tweet_raw in tweets_raw:
			#extract user info
			# user = tweet_raw['entities']['user_mentions']
			# if len(user)>0:
				# screen_name = user[0]['screen_name']
				# real_name = user[0]['name']
			screen_name = tweet_raw['user']['screen_name']
			real_name = tweet_raw['user']['name']

			#extract hashtags and put in the form of an array
			for hashtag_raw in tweet_raw['entities']['hashtags']:
				hashtags_temp.append(hashtag_raw['text'])

			#extract time of tweet creation and modify it to Isodate format
			created_at = tweet_raw['created_at'][4:-10]+tweet_raw['created_at'][-4:]
			created_at = datetime.datetime.strptime(created_at, "%b %d %H:%M:%S %Y")

			#putting it into structure that can be inserted into MongoDB
			tweets_mongo.append({'created_at':created_at,'screen_name':screen_name,'real_name':real_name,'hashtags':hashtags_temp})

			hashtags_temp=[] #reset the temp storage
 
# insert all extracted info into MongoDB
from pymongo import MongoClient
client = MongoClient()
client = MongoClient('localhost', 27017)
# client = MongoClient('mongodb://localhost:27017/')
db = client.w205assignment3
collection = db.tweets
collection.insert(tweets_mongo)
print('data loaded to mongodb')