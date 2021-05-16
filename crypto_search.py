#! /usr/bin/python

from googlesearch import search
import telegram_send
import yaml
import os
import os.path

## "Query used to search on Google"
query = 'latest news on bitcoin, ethereum and dogecoin cryptocurrency this week'

global nlist #this list will be pushed as telegram message to end user
global glist #this list will be used to keep track of all weblinks locally
nlist = [ ]
glist = [ ]

## "File 'saved_list.txt' is used to keep local track of weblinks"
if os.path.exists('/storage/emulated/0/Documents/saved_list.txt'):
	print("file exists")
else:
	print("file does not exist")	
	open("/storage/emulated/0/Documents/saved_list.txt",'w+').close()
  print ("created new blank file")
  
try:
	with open("/storage/emulated/0/Documents/saved_list.txt", 'r') as f:
		for line in f:
			print ("inside for loop")
			stripline =line.strip()
			print(stripline)
			glist.append(stripline)
except:
	print('ended with exception')
				
#print ("base glist")
#print (glist)
#print ("base nlist")
#print (nlist)

## "Deleting exitsing file after use"
if os.path.exists('/storage/emulated/0/Documents/saved_list.txt'):
	os.remove("saved_list.txt")
	print("file is now removed for next iteration")
else:
	print("unable to find file")


for i in search(query, tld='com', num=5, stop=20):
    print(i)
    if (len(i) > 70 and i in glist):
    	print("found match in existing file\n")
    elif (len(i) > 70 and i not in glist):
    	print("found new link..adding to file\n")
    	nlist.append(i)
    	glist.append(i)
    	nlist.append("")
    else:
    	print("link length less than required")


## "Saving updated weblinks to local file saved_list.txt"
file = open("/storage/emulated/0/Documents/saved_list.txt", 'w')
for n in glist:
	file.write(str(n) +'\n')
file.close()		

## "Converting List to Yaml format for better view"
result = yaml.dump(nlist)

## "Pushing yaml file as message to end User via Telegram_send api." 
## "An initial connection setup is required between server running this script and end user Telegram Bot using HTTP API token and passkey"
## 'If no new weblink is found in current iteration, a text message will be sent notifying the same"
if not nlist:
	telegram_send.send(messages=["Can't fetch any new links for your query on googlesearch. I will get back to you in another 4 hrs........"])
else:
	telegram_send.send(messages=[result])	


	
	
