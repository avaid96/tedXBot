import requests
import re
from bs4 import BeautifulSoup
from pprint import pprint
import urllib2
import random
import os
import sys
import json
import pyrebase

################## scraper functions ##################

def getfirsttalk(page):
    '''
    page is the html page from which we want to scrape.
    Function gets the first talk from the page.
    '''
    soup = BeautifulSoup(page.text, "html.parser")
    talklinks = soup.find_all("a", href=re.compile('/talks/'))
    parsedlinks = []
    for o in talklinks:
        parsedlinks.append(o['href'])
    parsedlinks = list(set(parsedlinks))
    return parsedlinks[0]

def SearchTedx(entry):
	'''
    input will be a search term for a video, and this returns the search URL
    '''
	url = "https://www.ted.com/search?cat=talks&per_page=12&q="
	word_add = ""
	split_word = entry.split()
	n = len(split_word)
	word_add = split_word[0]
	for i in range (1, int(n)):
		word_add = word_add + "+"+split_word[i]
	return url+word_add

def getFirstLink(URLstr):
	'''
	Return link to first video on the search URL page
	eg input: https://www.ted.com/search?cat=talks&per_page=12&q=politics
	'''
	page = urllib2.urlopen(URLstr).read()
	soup = BeautifulSoup(page,"html.parser")
	x=soup.findAll("a","visible-url-link")
	if len(x) < 1:
		return "No videos found"
	randomVid = random.choice(x)
	return randomVid.text #do .get('href') if you only want "/talks/..."
	
#Currently dangling
def getUserInfo(userID):
    '''
    Return user information in Json given the user's ID
    '''
    param = {
        "access_token": os.environ["PAGE_ACCESS_TOKEN"]
    }
    url="https://graph.facebook.com/v2.6/"+userID
    x=requests.get(url, params=param)
    data=x.json()
    return data

################## database functions ##################

def storeUser(userid, db, dbuser):
	'''Takes a userid (from the facebook graph api), an initialised firebase
	 database and an authenticated firebase user as an input, and stores the userid onto the database.'''
	if db.get(dbuser['idToken']).val().has_key(userid) == False:
		db.child(userid).set(True, dbuser['idToken'])
	else:
		print "User already in database."

def removeUser(userid, db, dbuser):
	'''Takes a userid (from the facebook graph api) an initialised firebase
	 database and an authenticated firebase user as an input, and removes the user from the database.'''
	if db.get(dbuser['idToken']).val().has_key(userid):
		db.child(userid).remove(dbuser['idToken'])
	else:
		print "User does not exist."

def refreshUserToken(auth, dbuser):
	'''Firebase user idTokens expire in 1 hour. This function refreshes our token and returns the dbuser with refreshed token.
	Call this function before calling a removeUser() or storeUser() function to ensure our dbtoken never expires.
	Make sure you assign the return value to the global variable 'user' in app.py.
	example:
	
	user = refreshUserToken(auth, user)
	storeUser(userid, db, user)

	'''
	dbuser = auth.refresh(dbuser['refreshToken'])
	return dbuser

def getAllUsers(db, dbuser):
	'''Returns all users from Firebase database.'''
	allusers =  db.get(dbuser['idToken']).val()
	allusers.pop('dummy', None)
	return allusers

def getUser(userid, db, dbuser):
	'''Get particular user from firebase database.'''
	allusers = db.get(dbuser['idToken']).val()
	return allusers[userid]

