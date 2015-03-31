# W205_ArthurMak

This is my repository for submitting the assignment for W205.
Information for assignment: https://github.com/alexmilowski/data-science

Assignments completed: 
- Assignment #1: Getting Started
- Assignment #2: Tweet Acquisition
- Assignment #3: Organizing Tweets


Assignment 3 

PLEASE READ "Write-up.docx" for the write-up of UML ERD, task#2 for each of the database categories, and code implementation with results using MongoDB.

INSTRUCTIONS FOR RUNNING THE CODE:
•	Setup mongo by doing the following:
-	Run “sudo mongod”
-	Run “mongo” on separate terminal to open mongo console
-	Inside mongo console, type:
o	use w205assignment3
o	db.createCollection('tweets')
•	Run the command “python load.py” to load the 2 JSON files into MongoDB (you can type “db.tweets.find()” in mongo console to double-check if data actually got loaded into the MongoDB)
•	Run the command “node app.js” to conduct the 3 queries for the 3 questions asked. 




Assignment #2 notes:

1. Run "python acquire.py" at terminal to create 7 text files of the tweets for the week
(eg. tweets_1_2015-01-28.txt)
2. Run "word.count.py" to create 3 csv files of words (words.csv), 
hashtags (hashtags.csv), and usernames (usernames.csv)
3. Put all these csv files into an excel file (histogram.xls) to create all three
histograms
4. Tweet data can also be found at s3://irclassbucket/assignment2

Reference:
See all sample tweet data and csv data in the "Data" folder
