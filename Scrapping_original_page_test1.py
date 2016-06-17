from bs4 import BeautifulSoup
import urllib
import os, csv
import mechanize
from sys import argv
from lsapi import lsapi

#the following code is specifically designed for Google Image Search
def web_scrapper(url):
    browser = mechanize.Browser()   # browser or mechanize used to cheat search engine
    browser.set_handle_robots(False)
    browser.addheaders = [('User-agent','Mozilla')]
    r = browser.open(url).read()
    i = 0
    soup = BeautifulSoup(r, "html.parser")
    res = soup.find('div', id='ires')
    letters = res.find_all('td')
    lobbying = {}
    for element in letters:
        x = {}
        x['href'] = str(element.a['href'].encode('ascii','replace').decode('ascii')[7:])
        x['alt'] = element.a.img['alt'].encode('ascii','replace').decode('ascii')
        x['src'] = element.a.img['src'].encode('ascii','replace').decode('ascii')
        x['domain'] = str(element.br.cite['title'].encode('ascii','replace').decode('ascii'))
        x['size info'] = element.br.br.br.get_text().encode('ascii','replace').decode('ascii')
        lobbying[url+" "+x['src']] = x
    return lobbying

def api_info(lobbying):
    l = lsapi('mozscape-295a2fa4c3', '95ef534d72971f96f3fd5776819a50f7')
    for key in lobbying.keys():
        print lobbying[key]['href']
        mozMetrics = l.urlMetrics(lobbying[key]['href'])
        lobbying[key]['inbound links'] = mozMetrics['uid']
        lobbying[key]['moz page rank'] = mozMetrics['umrp']
        lobbying[key]['moz subdomain rank'] = mozMetrics['fmrp']
        mozMetrics_domain = l.urlMetrics(lobbying[key]['domain'])
        lobbying[key]['domain inbound links'] = mozMetrics_domain['uid']
        lobbying[key]['domain page rank'] = mozMetrics_domain['umrp']
        print(lobbying[key])
    return lobbying

a = web_scrapper('https://www.google.com/search?q=duke&biw=1920&bih=958&source=lnms&tbm=isch&sa=X&ved=0ahUKEwiSzvHtkvnMAhVJU1IKHSKUDvsQ_AUIBygC')
print api_info(a)
#def output_data(url, save):
        
        
