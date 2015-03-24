'''
Instructions:

1. Run "python acquire.py" at terminal to create 7 text files of the tweets for the week
(eg. tweets_1_2015-01-28.txt)
2. Run "word.count.py" to create 3 csv files of words (words.csv), 
hashtags (hashtags.csv), and usernames (usernames.csv)
3. Put all these csv files into an excel file (histogram.xls) to create all three
histograms
4. Tweet data can also be found at s3://irclassbucket/assignment2

References:
- See all sample tweet data and csv data in the "Data" folder

'''

import sys
import os
import re #regular expression library

# f=open('tweets_6_2015-01-31.txt','r')	

words = {}
hashtags = {}
usernames ={}

#counting function
def count(w,d): #w=word, d=dictionary
	if w in d:
		d[w] += 1  #add 1 to the current count for that word
	else:
		d[w] = 1   #add the word to the dictionary with a count of 1

#csv output function
def writeCSV(fname,list):
	csvFile = open(fname+'.csv',"w")
	for word, times in list.items():
		csvFile.write('"'+word+'","'+str(times)+'"\n')
	csvFile.close()

for filename in os.listdir("."):  #loop through each file in current directory
	if filename.endswith(".txt"): #only interact with those with specific extension
		f = open(filename.strip(),"r")
		for line in f:
			for word in line.split():
				#make sure word is converted from list to string
				while isinstance(word, list):
					word=word[0]
				#make sure lowercase so that capitalized and non-capitalized words are not double-counted
				word=word.lower()
				#remove punctuations that attach themselves to the end of the string
				while word.endswith('!') or word.endswith('?') or word.endswith(',') or word.endswith('.') or word.endswith(':') or word.endswith('_') or word.endswith('"'): 
					word=word[:-1]
				#remove certain punctuations that attach themselves to the beginning of the string
				while word.startswith('"'):
					word=word[1:]
				if len(word)>0:
					# only store words after getting rid of certain non-useful words
					if word!=',' and word!=' ' and word!='.' and word!='-' and word!='+'\
						and word !='[' and word !=']' and word !='...' and word!='='\
						and not ('/' in word) and not ('\\' in word) \
						and not ('\xe2' in word) and not ('\xef' in word) and not ('\xd0' in word)\
						and not ('\xc2' in word) and not ('\xf0' in word) and not ('\xe3' in word): 
							# store hashtags in separate list
							if word[0]=='#':
								count(word,hashtags)
							# store usernames in separate list
							elif word[0]=='@':
								count(word,usernames)
							# store word in separate list if all conditions passed
							else:
								count(word,words)
     
# print words.items()
# print hashtags.items()
# print usernames.items()
writeCSV("words",words)
writeCSV("hashtags",hashtags)
writeCSV("usernames",usernames)


