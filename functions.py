import requests
import re
from bs4 import BeautifulSoup
from pprint import pprint
import urllib2


def getfirsttalk(page):
    '''page is the html page from which we want to scrape.
    Function gets the first talk from the page.'''
    soup = BeautifulSoup(page.text, "html.parser")
    talklinks = soup.find_all("a", href=re.compile('/talks/'))
    parsedlinks = []
    for o in talklinks:
        parsedlinks.append(o['href'])
    parsedlinks = list(set(parsedlinks))
    return parsedlinks[0]

def SearchTedx(entry):
	'''input will be a search for a video and returns the url for the list of all 
	based on input'''
	url = "https://www.ted.com/search?cat=talks&per_page=12&q="
	word_add = ""
	split_word = entry.split()
	n = len(split_word)
	word_add = split_word[0]

	for i in range (1, int(n)):
		url += word_add + "+"+split_word[i]

	return url

def getFirstLink(URLstr):
	'''
	Return link to first video on the search page (URLstr)
	eg input: https://www.ted.com/search?cat=talks&per_page=12&q=politics
	'''
	page = urllib2.urlopen(URLstr).read()
	soup = BeautifulSoup(page,"html.parser")
	x=soup.findAll("a","visible-url-link")
	return x[0].text #do x[0].get('href') if you only want "/talks/..."
	
