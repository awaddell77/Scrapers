from bs4 import BeautifulSoup as bs
import lxml
import requests
import urllib, urllib2, unicodedata
import csv
import unicodedata
from soupclass6 import *
import sys

'''FOR SCRAPING CARD DATA FROM WEISS SCHWARZ (ws-tcg.com)


03/17/16
-Added test and stsc functions

4/08/16
-The test function now returns the link to the picture on the website for each card under the "Picture" dictionary key
-"Upgraded" this scraper's library from soupclass5 to soupclass6  
4/12/16
-Changed tablefind function so that it no longer returns just the table but the whole site in order to help scrape the image 
'''

def main_true(x):
    urls = text_l(x)
    results = [['Card Name','Power', 'Type', 'Color', 'Card Text', 'Level', 'Soul', 'Rarity', 'Trigger', 'Traits', 'Cost', 'Card Number', 'Side', 'Expansion']]
    for i in range(0, len(urls)):
        #iterates through all of the fresh links
        print("Now Processing %s" % urls[i])
        bsObject = test(tablefind(urls[i]))
        results.append(stsc(bsObject))
    w_csv(results)
    return "Complete"

def main_s1(x):#for singles (using test/stsc function instead of soupmaker/td_sp_img)
    table = test(tablefind((x)))
    info = stsc(table)
    return info

def m_links1(x):#for links, takes url for link page (USES THE TEST FUNCTION INSTEAD OF td_sp_img)
    results = [['Card Name','Power', 'Type', 'Color', 'Card Text', 'Level', 'Soul', 'Rarity', 'Trigger', 'Traits', 'Cost', 'Card Number', 'Side', 'Expansion']]
    urls2 = []
    urls = text_l(x)#list of urls
    for i in range(0, len(urls)):
        links = soupmaker(urls[i])
        links = links.find('div', {'id':'expansionDetail_table'})
        urls2.extend(link_s(links))#list should contain all of the links inside of those url tables
    for i in range(0, len(urls2)):
        #iterates through all of the fresh links
        print("Now Processing %s" % urls2[i])
        bsObject = test(tablefind(urls2[i]))
        results.append(stsc(bsObject))
    w_csv(results)
    return "Complete"

def main_list(x):#if you already have all the links for each card then use this one
    results = []
    urls = text_l(x)
    for i in range(0, len(urls)):
        bsObject = soupmaker(urls[i])
        results.append(td_sp_img(bsObject))
    w_csv(results)
    return "Complete"
    
    
'''B-SOUP STUFF'''
def soupmaker(x):#makes the soup
    url = x
    html = requests.get(url)
    html = html.content
    bsObject = bs(html, 'lxml')
    return bsObject
                 
def tablefind(x):#isolates table
    url = x
    url = requests.get(url)
    url = url.content
    bsObject = bs(url, 'lxml')
    #table = bsObject.find('div', {'id': 'cardDetail'})
    return bsObject

def test(x):#is fed table
    bsObject = x
    table = bsObject.find('div', {'id': 'cardDetail'})
    headers = table.find_all('th')
    d={}
    for i in range(0, len(headers)):
        cell = headers[i].find_next_sibling()
        d[S_format(headers[i].text).encoder()] = cell
    d['Picture Link'] =  S_format(str(bsObject.find('td', {'class':'graphic'}).img)).linkf('src=')
    d['Picture'] = fn_grab(d['Picture Link'])
    return d
        
    
    
'''FORMATTING'''
def stsc(x):#takes dictionary
    d = x
    d['Card Name'] = d['Card Name'].span#prevents text method from doubling the name
    need_1 = ['Card Name','Power', 'Card Type', 'Color', 'Text', 'Level', 'Soul', 'Rarity', 'Trigger', 'Special Attribute', 'Cost', 'Card No.', 'Side', 'Expansion', 'Picture', 'Picture Link']
    pict = ['Color','Trigger','Soul', 'Side']
    need_2 = ['Card Name','Power', 'Card Type', 'Text', 'Level', 'Rarity', 'Special Attribute', 'Cost', 'Card No.', 'Expansion']#need list sans the pictures
    for i in range(0, len(pict)):
        if pict[i] == 'Color' or pict[i] == 'Side':
            new = S_format(str(d[pict[i]].img)).linkf('<img src=').split('/')
            d[pict[i]] = new[len(new)-1]
        else:
            d[pict[i]] = len(d[pict[i]].find_all('img'))
    for i in range(0, len(need_2)):
        d[need_2[i]] = re.sub('\n''\r''\t',d[need_2[i]].text)
    
    return S_format(d).d_sort(need_1)

def dup_erase(x):#accepts list, returns duplicate free version
    l_1 = []
    bad = ['poll', 'vote', '', 'wrong website?', 'Show More &raquo', None]
    for i in range(0, len(x)):
        if x[i] not in l_1 and x[i] not in bad:
            l_1.append(x[i])
    return l_1
     


def encoder(x):#takes text from bsObject tag(s) and converts into unicode-free strings
    h = x
    try:
        h = x.encode('ascii', 'ignore')
        #print 'Tried to encode' #for testing
    except UnicodeEncodeError as U:
        h = h.encode('utf-8', 'ignore')
        print 'UTF-8'
        return h
    else:
        h = x.encode('ascii', 'ignore')#changed to replace
        print 'ASCII'
        return h

def img_n(x):#takes image tag (MUST BE STRING) and extracts the image file name
    l =[]
    im = ''
    im_s = x.split('"')
    for i in range(0, len(im_s)):
        if im_s[i] == '<img src=' or im_s[i] == ' <img src=' or im_s[i] == ' src=':
            im = im_s[i+1] #im is the location + the file name
            print im
    l = im.split('/')
    f_name = l[len(l)-1] #last item in the directory = file name
    return f_name

def w_rem(x, y):#removes x from list, returns new list (y is the element that is going to be removed)
    l = x
    while y in l:
        l.remove(y)
    return l
def spacer(x):
    n_s = x
    while '\n' in n_s:
        n_s = x.replace('\n', ' ')
    return n_s
        
'''LINK SCRAPING'''
def linkf(x):#takes link tag (MUST BE STRING) and extracts the link
    l =[]
    ln = ''
    ln_s = x.split('"')
    for i in range(0, len(ln_s)):
        if ln_s[i] == '<a href=' or ln_s[i] == ' href=':
            if ln_s[i+1] != 'javascript:void(0);':
                ln = ln_s[i+1] #ln is the link (still needs to be joined witht the base URL
    ln = base_url(ln)

    #ln = b_url + ln #MAJOR WORKAROUND!!!! IN THE FUTURE THS SHOULD CALL A FUNCTION THAT FINDS THE BASE
    return ln

def link_s(x):#takes bsObject with isolated link table and scrapes links
    links = x
    links = x.find_all('a')#added
    l = []
    n_l = []#for the full url
    bad_l = ['www.amazon.com', 'www.amazon.co.uk', '']
    for i in range(0, len(links)):
        link1 = linkf(str(links[i]))
        if link1 not in bad_l and link1 not in l:
            l.append(linkf(str(links[i])))
        
    l = dup_erase(l) #added        
    return l

def base_url(x):#x is the url
    if x == '' or x == None:
        return
    
    base = 'http://ws-tcg.com/en/cardlist/list/'
    url = x
    url = x.split('/',1)
    print url
    f_url = base + url[1]
    return f_url
    
    
    
    
    

'''I/O'''

def w_csv(x):#accepts lists of other lists, spits out CSV file
    csv_out = open('WSfile.csv', 'wb')
    mywriter = csv.writer(csv_out)
    print "This is x: %s" % (x)
    mywriter.writerows(x)
    csv_out.close()
    return

def text_l(x):#reads text file, returns list of elements
    words = ''
    l = []
    with open(x, 'r') as f:
        data = f.readlines()
        for line in data:
            words = line.split()
            print words
            l.extend(words)
        print l
        return l
    

if len(sys.argv) != 1:
    if sys.argv[1] == '-mt':
        main_true(sys.argv[2])
    m_links1(sys.argv[1])F