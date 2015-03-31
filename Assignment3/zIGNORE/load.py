import sys
import os
import json

for filename in os.listdir("."):  #loop through each file in current directory
	if filename.endswith(".json"): #only interact with those with specific extension
		f = open(filename.strip(),"r")
		data = json.load(f)
		# print data		
		# for key in data:
		# 	print key
		# 	print '\n'
			# print data[key]

