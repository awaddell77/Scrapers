import lxml, requests
from bs4 import BeautifulSoup as bs
import csv
from soupclass8 import *
import sys
'''NOTES: 2/10/2016
-
-Moved bsObject into main function in order to decrease redundant get requests
-Added thtd function which theoretically allows program to grab the cells of tables with the th-td configuration
'''



def main(x, links=0):#batch
    
    
    if links != 0:
        urls = x
    else: 
        urls  = text_l(x)
    t_results = [['Name', 'ATK/DEF', 'Monster Type','Card Type', 'Passcode', 'Level','Attribute','Card Text','Set']]
    for i in range(0, len(urls)):
        bsObject = soupmaker(urls[i])
        a_table = sfind(bsObject)
        if a_table == 'The page is not up.':
        	t_results.append([a_table])
        elif len(a_table) == 2:
            b_rows = thtd(a_table[0])
            b_rows.append(encoder(a_table[1].text).translate(None, '\n'))
            t_results.append(b_rows)
        else:
            b_rows = thtd(a_table)
            t_results.append(b_rows)
    w_csv(t_results)
    print(t_results)
    return "Complete"

def main_s(x): #singles
    urls = [x]
    t_results = []
    for i in range(0, len(urls)):
        bsObject = soupmaker(urls[i])
        a_table = sfind(bsObject)
        if len(a_table) == 2:
            b_rows = thtd(a_table[0])
            b_rows.append(encoder(a_table[1].text).translate(None, '\n'))
            t_results.append(b_rows)
        else:
            b_rows = thtd(a_table)
            t_results.append(b_rows)
    #w_csv(none_remover(t_results))
    return(t_results)

def remover(x):
    l = []
    if x == None:
        return "None"
    for i in range(0, len(x)):
        if x[i] != None:
            l.append(x[i])
        else:
            l.append("None")
    return l

def none_remover(x):
    none_c = 0
    n = x
    for i in range(0, len(x)):
        if n[i] == None:
            n[i] = [["Number %d was not found" % (i)]]
            none_c = none_c + 1
    print ("%d entries were not found." % (none_c))
        
    return n
        
        
    
def soupmaker(x):#makes the soup
    url = x
    html = requests.get(url)
    html = html.content
    bsObject = bs(html, 'lxml')
    return bsObject

def sfind(x, effect = 0):#isolates the parent tag that contains the tables
    bsObject = x
    if bsObject.find('table',{'class':'cardtable'}) == None and bsObject.find('table', {'class':'navbox hlist'}) == None:
    	return 'The page is not up.'
    table = bsObject.find('table',{'class':'cardtable'})
    table2 = bsObject.find('table', {'class':'navbox hlist'})#the english description
    if table2 == None:
        return table
    else:
        return table,table2

def encoder(x):#takes text from bsObject tag(s) and converts into unicode-free strings
    h = x
    try:
        h = x.encode('ascii', 'ignore')

        #print 'Tried to encode' #for testing
    except UnicodeEncodeError as U:
        h = h.encode('utf-8', 'ignore')
        print('UTF-8')
        return(h)
    except AttributeError as E:
        print(E)
        return x
    print('ASCII')
    return h

def dup_erase(x):#accepts list, returns a list that does not containt any elements in the "bad" list
    l_1 = []
    bad = ['Flavor Text:', 'Sets:', 'Kanji:', 'Illust:', 'Other related pages:', 'Gallery Tips Rulings Errata Trivia Character', 'Gallery Tips Rulings', 'Errata Trivia Character']
    for i in range(0, len(x)):
        if x[i] not in bad:
            l_1.append(x[i])
    return l_1

def thtd(x):
    l = []
    d ={}
    bsObject = x
    headers = bsObject.find_all('th')
    for i in range(0, len(headers)):
        if headers[i].next_sibling != None:
            try:
                d[encoder(headers[i].text).translate(None, '\n')] = encoder(headers[i].next_sibling.text).translate(None, '\n')
            except AttributeError as AE:
                d[encoder(headers[i].text).translate(None, '\n')] = "None"
    print(d)
    return d_sort(d)#creates a list from dictionary and then removes non-list elements
        
        


def d_sort(x):
    d = x
    n_l = []
    criteria = ['English', 'ATK / DEF', 'Types','Type', 'Card Number', 'Level', 'Attribute', 'Passcode']
    default = "Not Available"
    for i in range(0, len(criteria)):
        n_l.append(d.get(criteria[i], default))
    l = d.keys()
    return n_l

        
def text_l(x):
    words = ''
    l = []
    with open(x, 'r') as f:
        data = f.readlines()
        for line in data:
            words = line.split()
            print(words)
            l.extend(words)
        print(l)
        return l

        
        
def w_csv(x):#accepts lists of other lists, spits out CSV file
    csv_out = open('YGOfile1.csv', 'wb')
    mywriter = csv.writer(csv_out)
    print ("This is x: %s" % (x))
    mywriter.writerows(x)
    csv_out.close()
    return

def csv_ext(x,n):#n is cell number/location within the list where the needed info is located
    l = []
    for i in range(0, len(x)):
        items = x[i]
        l.append(items[n])
    return l
        


def linkf(x):#takes link tag (MUST BE STRING) and extracts the link
    l =[]
    ln = ''
    ln_s = x.split('"')
    for i in range(0, len(ln_s)):
        if ln_s[i] == '<a href=' or ln_s[i] == ' <a href=':
            ln = ln_s[i+1] #ln is the link (still needs to be joined witht the base URL
    #ln = b_url + ln #MAJOR WORKAROUND!!!! IN THE FUTURE THS SHOULD CALL A FUNCTION THAT FINDS THE BASE
    return ln

def ygo_link_grab(x, card_name):
    url = x
    if S_base(url).soupmaker().find(string=re.compile(card_name)) == None:
        return 'None found'
    else:
        site = S_base(url).soupmaker()
        item = site.find(string=re.compile(card_name))
        table = S_table(site).table_find(item) #test
        if table != False:
            links_r = S_table(table).table_eater_exp('a',1, 4)
            links = ['http://yugioh.wikia.com' + S_format(str(links_r[i])).linkf('<a href=') for i in range(0, len(links_r))]
            text_wc(links)
            return links

if len(sys.argv) > 1:
    if sys.argv[1] == '-b':
        main(sys.argv[2])
    elif sys.argv[1] == '-t':
        main(ygo_link_grab(sys.argv[2], sys.argv[3]), 1)
