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
