import requests
import re
from bs4 import BeautifulSoup
from pprint import pprint
import urllib2
import os
import sys
import json

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
	return x[0].text #do x[0].get('href') if you only want "/talks/..."

def getUserInfo(userID):
    '''
    Return user information in Json given the user's ID
    '''
    #use os.environ("PAGE_ACCESS_TOKEN") when works
    param = {
        "access_token": "EAACEdEose0cBALRBZBaZAkP8pErwXQ192SZBY52FIXDk5ErTXZB6VoRwWkXSv2lFs1O4YGXt8oxSYg2UDxTPwSbHZAaJ1Pkwly7zjOHaHrDdGU1rA62wpt76te5frMBXCNSbWkolNd8Gf2DlQg9UTr1pcQJMzGUcmaWgRF0SaCr9qv9GpOkLURZCBt0KvDgZCEZD"
    }
    url="https://graph.facebook.com/v2.6/"+userID
    x=requests.get(url, params=param)
    data=x.json()
    return json.dumps(data)
