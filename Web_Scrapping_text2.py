from bs4 import BeautifulSoup
import urllib
import os, csv
import mechanize
from sys import argv


def web_scrapper(url):
    browser = mechanize.Browser()   # browser or mechanize used to cheat search engine
    browser.set_handle_robots(False)
    browser.addheaders = [('User-agent','Mozilla')]
    r = browser.open(url).read()
    i = 0
    soup = BeautifulSoup(r, "html.parser")
    letters = soup.find_all("img")
    lobbying = {}
    for element in letters:
        keyset=element.attrs
        x = {}
        if ("alt" in keyset):
            x ["alt"] = element["alt"].encode('ascii','replace').decode('ascii')
        else:
            x ["alt"] = ""
        if ("height" in keyset):
            x ["height"] = element["height"].encode('ascii','replace').decode('ascii')
        else:
            x["height"] = 0
        if ("width" in keyset):
            x ["width"] = element["width"].encode('ascii','replace').decode('ascii')
        else:
            x ["width"] = 0
        if ("src" in keyset):
            lobbying[url+element["src"].encode('ascii','replace').decode('ascii')] = x
 #          urllib.urlretrieve(element["src"], os.path.basename(element["src"]))
        else:
            lobbying[url+str(i)] = x
            i = i+1
        #whether to do it this way for src depends on the wepage
        #Obviously for Bing you can just use src without adding url

    return lobbying

# the following function requires you to create a file callsed lobbying.csv before running the script
def output_data (url, save):
    lobbying = web_scrapper(url)
    os.chdir(save)
    with open("lobbying.csv", "w") as toWrite:
        writer = csv.writer(toWrite, delimiter=",")
        writer.writerow(["src", "alt", "height", "width"])
        for a in lobbying.keys():
            writer.writerow([a, lobbying[a]["alt"], lobbying[a]["height"], lobbying[a]["width"]])

output_data("https://www.google.com/search?q=duke&biw=1440&bih=778&source=lnms&tbm=isch&sa=X&ved=0ahUKEwi2-q7Z4_XMAhVIVj4KHTySAQgQ_AUIBygC", "/Users/David/Documents/Undergraduate/Data+_Search_Algorithms")

csvfile = argv[1]
save = argv[2]
csvdata = csv.reader(open(csvfile))
os.chdir(save)
with open("lobbying.csv", "w") as toWrite:
    writer = csv.writer(toWrite, delimiter=",")
    writer.writerow(["src", "alt", "height", "width"])
    for row in csvdata:
        url = row[0]
        lobbying = web_scrapper(url)
        for a in lobbying.keys():
            writer.writerow([a, lobbying[a]["alt"], lobbying[a]["height"], lobbying[a]["width"]])



