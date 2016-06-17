from bs4 import BeautifulSoup
import urllib
import os, csv
import math
from sys import argv
from textblob import TextBlob as tb

url1 = tb(" ")
url2 = tb(" ")
url3 = tb(" ")
def web_scrapper(url):
    #browser = mechanize.Browser()   # browser or mechanize used to cheat search engine
    browser.set_handle_robots(False)
    browser.addheaders = [('User-agent','Mozilla')]
    r = browser.open(url).read()
    i = 0
    soup = BeautifulSoup(r, "html.parser")
    return soup
def tf(word, blob):
    return blob.words.count(word) / len(blob.words)

def n_containing(word, bloblist):
    return sum(1 for blob in bloblist if word in blob.words)

def idf(word, bloblist):
    return math.log(len(bloblist) / (1 + n_containing(word, bloblist)))

def tfidf(word, blob, bloblist):
    return tf(word, blob) * idf(word, bloblist)

bloblist = [url1, url2, url3]
for i, blob in enumerate(bloblist):
    print ("Top words in url {}". format(i + 1))
    scores = {word: tfidf(word, blob, bloblist) for word in blob.words}
    sorted_words = sorted(scores.items(), key = lambda x: x[1], reverse = True)
    for word, score in sorted_words[:3]:
        print ("\tWord: {}, TF-IDF: {}" .format(word, round(score, 5)))
