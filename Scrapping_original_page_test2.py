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
        href = str(element.a['href'].encode('ascii','replace').decode('ascii')[7:])
        pos = href.find('&')
        if pos != -1:
            href = href[:pos]
        x['href'] = href
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

def supper_scrapper(url):
    a = web_scrapper(url)
    return api_info(a)

def complete_scrapper(lobbying, url,i):
    if i==0:
        return lobbying
    else:
        new_data = supper_scrapper(url)
        lobbying.update(new_data.copy())
        browser = mechanize.Browser()   # browser or mechanize used to cheat search engine
        browser.set_handle_robots(False)
        browser.addheaders = [('User-agent','Mozilla')]
        r = browser.open(url).read()
        soup = BeautifulSoup(r, "html.parser")
        res = soup.find('div', id='foot')
        letters = res.find_all('td', class_='b')[1]
        next_item = letters.a
        new_url = 'https://www.google.com'+next_item['href']
        return complete_scrapper(lobbying, new_url, i-1)
        
print complete_scrapper({},'https://www.google.com/search?q=duke&biw=1440&bih=734&source=lnms&tbm=isch&sa=X&ved=0ahUKEwielvCX8vrMAhULVD4KHdN9CVYQ_AUIBygC' , 3)
#a = web_scrapper('https://www.google.com/search?q=duke&biw=1920&bih=958&source=lnms&tbm=isch&sa=X&ved=0ahUKEwiSzvHtkvnMAhVJU1IKHSKUDvsQ_AUIBygC')
#print api_info(a)
#def output_data(url, save):

csvfile = argv[1]
save = argv[2]
csvdata = csv.reader(open(csvfile))
os.chdir(save)
with open('lobbying.csv','w') as toWrite:
    writer = csv.writer(toWrite, delimiter=',')
    writer.writerow()
    for row in csvdata:
        url = row[0]
        lobbying = complete_scrapper({}, url, 10)
        for a in lobbying.keys():
            writer.writerow([a, ])
        
