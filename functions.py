import requests
import re
from bs4 import BeautifulSoup
from pprint import pprint


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




keyword = raw_input("Search Video: ")
url = "https://www.ted.com/search?cat=talks&per_page=12&q="
word_add = ""
def SearchTedx(entry):
	'''input will be a search for a video and returns the url for the list of all 
	based on input'''
	split_word = entry.split()
	n = len(split_word)
	word_add = split_word[0]

	for i in range (1, int(n)):
		word_add = word_add + "+"+split_word[i]

	

	print (url)
	print (word_add)
	print (url + word_add)
	print split_word[0]
	print n


SearchTedx(keyword)