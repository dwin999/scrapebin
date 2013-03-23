#!/usr/bin/env python
import sqlite3 as lite
import sys
import time 
import os.path
import urllib
from datetime import datetime
import mechanize
########Database Functions########
def create_db(today): 		
	if os.path.isfile(today) <= 0:
		con = lite.connect(today)

		with con:
			cur = con.cursor()
			cur.execute("CREATE TABLE PasteBin(link TEXT,title TEXT, data TEXT,timestamp TEXT)")
		con.close()
# if the database file does not exist create it :D	
def addtodb(link,data,title):
	timestamp = datetime.now().strftime("%Y-%m-%d %H:%M %Z") 
	con = lite.connect(today)# connect n insert data into sqllite db
	con.cursor().execute("INSERT INTO PasteBin VALUES (?,?,?,?)", (buffer(link),buffer(title),buffer(data),buffer(timestamp)))
	con.commit()
######Scraping function####################
def scrape_links(url,title):
	br = mechanize.Browser()
	br.set_proxies({"http": "127.0.0.1:3128"})
	br.addheaders = [('User-agent', 'Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)')]
	br.set_handle_robots(False)
	br._factory.is_html = True
	try:
		br.open(url,timeout=30.0)
		data = br.response().read()
		addtodb(url,data,title)
	except:
	      print "Failed to download " + url

#####Main Program###############
today = datetime.now().strftime("%Y-%m-%d") + ".db"
url_dict = {}
counter = 0
#debug = 0
while True:
	create_db(today)
	br = mechanize.Browser()
	br.set_proxies({"http": "127.0.0.1:3128"})#tor support
	br.addheaders = [('User-agent', 'Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)')]
	br.open('http://pastebin.com/archive', timeout=30.0)
	s = time.time()
	for link in br.links():
		
		
		if((len(link.url) == 9) and ((link.url == "/settings") != 1)):
			raw_url ="http://pastebin.com/raw.php?i="+str(link.url[1:9])
			# if the dictaoinry has not got the key in the index it won't scrape it 
			if not (url_dict.has_key(raw_url)):
				scrape_links(raw_url,(str(link.text)))
				url_dict[raw_url] = ' Link Checked'
				time.sleep(1)
				print raw_url + " Checked" 
				#print "Number of links scraped" + str(debug) + "Time since start" + str(time.time() - s)
				#debug+=1 
			#else:
				#print "Link already checked"
	if(counter == 5):
		url_dict.clear() # clear the dictionary every 5 scrapes
	counter+=1
		
	
#super fun maths...pastebin archive has 250 links. They expire around in around 10mins.
#Thats 540 seconds so i have a delay of 1 to account for time to download scrapes
