import urllib, urllib2, lxml, requests
from bs4 import BeautifulSoup as bs
import csv
 
url = 'http://buddyfight.wikia.com/wiki/Purgatory_Knights,_Eraser_Hand_Dragon'
url = requests.get(url)
url = url.content
bsObject = bs(url, 'lxml')
 
bsObject.find('wsCategories')
bsObject.find('table',{'class':'main'}) #the table
table = bsObject.find('table',{'class':'main'}) #for later
#name of the card
bsObject.find('table',{'class':'main'}).td.findNextSibling('td')
'''NOTES: 2/10/2016
-
-Moved bsObject into main function in order to decrease redundant get requests
-Added thtd function which theoretically allows program to grab the cells of tables with the th-td configuration
'''

'''def main_t(x): #for the big table
    l = []
    table1 = soupmaker(x)
    tr = table1.find('tr')
    for i in range(0, len(table1.find_all('tr'))):
        l.append(td_sort(tr))
        tr = tr.findNext('tr')
    return l
            


def td_sort(x):#accepts rows then sorts through cells
    l = []
    l_flag = 0
    cells = x.find('td')
    for i in range(0, len(x.find_all('td'))):
        l.append(cells)
        if l_flag != 1:
            l.append(main_s(linkf(str(cells.a))))
        elif l_flag == 1:
            return l
        else:
            cells = cells.findNext('td') '''

    
def main_ls(x):
    
    urls  = link_st(x)#pick between link_s and link_st
    t_results = []
    for i in range(0, len(urls)):
        a_table = sfind(urls[i])
        b_rows = td(a_table)#changed from tablesort
        t_results.append(b_rows)
        print "Number %d" % (i)
    #return t_results #for testing purposes
    w_csv(none_remover(t_results))
    return "Complete"


def main(x):#batch
    
    urls  = text_l(x)
    t_results = [['ATK/DEF','Name','Monster Type','Card Type', 'Passcode', 'Level','Attribute','Card Text','Set']]
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
    w_csv(t_results)
    print t_results
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
    return t_results
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
    print "%d entries were not found." % (none_c)
        
    return n
def tblsort(x):#top level sorter
    #section that contains the tables
    if x == None:
        return ['None']
    if x.find('td') == None:
        return ['None']
    table = x.find('td')
    l = []
    for i in range(0, len(x.find_all('td'))):
        l.append(tr_list(table))
        #l.append(table)
        table = table.findNext('table')
    return l
        
        
    
def soupmaker(x):#makes the soup
    url = x
    html = requests.get(url)
    html = html.content
    bsObject = bs(html, 'lxml')
    return bsObject

def sfind(x, effect = 0):#isolates the parent tag that contains the tables
    #url = x
    #url = requests.get(url)
    #url = url.content
    #bsObject = bs(url, 'lxml')
    bsObject = x
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
        print 'UTF-8'
        return h
    except AttributeError as E:
        print E
        return x
    else:
        h = x.encode('ascii', 'ignore')
        print 'ASCII'
        return h

def tr_list(x):#takes table returns list
    l = []
    rows = x.find('tr')#changed from 'tr')
    print table
    for i in range(0, (len(x.find_all('tr')))):
        if rows == None:
            l = dup_erase(l)
            return l
        else:
            l.append((encoder(rows.text).translate(None,'\n''\t')).strip(' '))
            rows = rows.findNext('tr')
    l = dup_erase(l)
    return l

def dup_erase(x):#accepts list, returns a list that does not containt any elements in the "bad" list
    l_1 = []
    bad = ['Flavor Text:', 'Sets:', 'Kanji:', 'Illust:', 'Other related pages:', 'Gallery Tips Rulings Errata Trivia Character', 'Gallery Tips Rulings', 'Errata Trivia Character']
    for i in range(0, len(x)):
        if x[i] not in bad:
            l_1.append(x[i])
    return l_1
def td(x, custom='NA'):#TO BE DONE: FIND ALL td from the main table and then just parse through them
    l = []
    d = {}
    if x == None:
        return None
    bad = ( 'Gallery Tips Rulings Errata Trivia Character', 'Character', 'Trivia', 'Errata', 'Gallery', 'Tips', 'Rulings', 'Illus:')
    table_c = x.find_all('td')
    
    for i in range(0, len(table_c)):
        #if table_c[i] not in bad:
        if i % 2 == 0:
            
            try:
                d[encoder(table_c[i].text).translate(None, '\n').strip(' ')] = encoder(table_c[i + 1].text).translate(None, '\n').strip(' ')
            except IndexError as IE:
                print d
                return d_sort(d)
                
           #l.append(encoder(table_c[i].text).translate(None, '\n').strip(' '))
    print d
    return d_sort(d)
    #return (l_maker(d_sort(d)))

def thtd(x):
    l = []
    d ={}
    bsObject = x
    #if bsObject.find_all('td') or bsObject.find_all('th') == None:
        #return None
    headers = bsObject.find_all('th')
    for i in range(0, len(headers)):
        #head, cell = headers[i], headers.find('td')
        if headers[i].next_sibling != None:
            try:
                d[encoder(headers[i].text).translate(None, '\n')] = encoder(headers[i].next_sibling.text).translate(None, '\n')
            except AttributeError as AE:
                d[encoder(headers[i].text).translate(None, '\n')] = "None"
                
        '''else:
            d[encoder(headers[i].text).translate(None, '\n')] = "None"'''
        #l.append(head,cel
    print(d)
    return d_sort(d)#creates a list from dictionary and then removes non-list elements
        
        
    
def d_keymaker(x):
    n_l = []
    for i in range(0, len(x), 2):
        n_l.append(x[i])
    d = dict.fromkeys(n_l)
    return d
def k_keymaker(x,y):#x is the dictionary, y is the list of new values
    keys = dict.keys(x)
    n_d = x
    l = y
    for i in range(0, len(x)):
        n_d[keys[i]] = l[i]
    return n_d

def d_sort(x):
    d = x
    n_l = []
    criteria = ['English', 'ATK / DEF', 'Types','Type', 'Card Number', 'Level', 'Attribute']
    default = "Not Available"
    for i in range(0, len(criteria)):
        n_l.append(d.get(criteria[i], default))
        #del d[criteria[i]]
    l = d.keys()
    '''for i in range(0, len(l)):
        if len(l[i]) > 12:
            n_l.append(l[i])'''
    return n_l
    
def l_maker(x):#sorts through elements of a list to check if those elements are lists
    l = []
    for i in range(0, len(x)):
        if isinstance(x[i], list) == True:
            l.extend([x[i]])
        '''else:
            l.append(x[i])'''
    return l
     
    
    
    
        
        
    
        
def text_l(x):
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
'''def sort1(x):#sorts through list deletes elements with specific keywords
    keyword = ["Kanji"]
    for i in range(0, len(x)):
        for l in'''
        
        
        
def w_csv(x):#accepts lists of other lists, spits out CSV file
    csv_out = open('YGOfile1.csv', 'wb')
    mywriter = csv.writer(csv_out)
    print "This is x: %s" % (x)
    mywriter.writerows(x)
    csv_out.close()
    return
def r_csv(x):
    l = []
    csv_in = open(x, 'rb')
    myreader = csv.reader(csv_in)
    for row in myreader:
        l.append(row)
    csv_in.close()
    return l
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

def link_s(x):#scrapes links
    page = soupmaker(x)
    links = page.find_all('a')
    l = []
    bad_l = ['http://buddyfight.wikia.com/wiki/Ancient_World', 'http://buddyfight.wikia.com/wiki/Danger_World',
             'http://buddyfight.wikia.com/wiki/Darkness_Dragon_World','http://buddyfight.wikia.com/wiki/Dragon_World',
             'http://buddyfight.wikia.com/wiki/Dungeon_World', 'http://buddyfight.wikia.com/wiki/Hero_World',
             'http://buddyfight.wikia.com/wiki/Katana_World', 'http://buddyfight.wikia.com/wiki/Legend_World',
             'http://buddyfight.wikia.com/wiki/Magic_World', 'http://buddyfight.wikia.com/wiki/Star_Dragon_World',
             'http://buddyfight.wikia.com/wiki/Monster', 'http://buddyfight.wikia.com/wiki/Flag',
             'http://buddyfight.wikia.com/wiki/Spell', 'http://buddyfight.wikia.com/wiki/Impact',
             'http://buddyfight.wikia.com/wiki/Item', 'http://buddyfight.wikia.com/wiki/SetList:BFE-H-BT04?action=edit', '']
    for i in range(0, len(links)):
        link1 = linkf(str(links[i]))
        if link1 not in bad_l:
            l.append(link1)
    return l
        
def link_st(x):#scrapes links
    page = soupmaker(x)
    table = page.find('table') #{'class':'wikitable sortable jquery-tablesorter'})
    links = page.find_all('a')
    l = []
    bad_l = ['http://buddyfight.wikia.com/wiki/Ancient_World', 'http://buddyfight.wikia.com/wiki/Danger_World',
             'http://buddyfight.wikia.com/wiki/Darkness_Dragon_World','http://buddyfight.wikia.com/wiki/Dragon_World',
             'http://buddyfight.wikia.com/wiki/Dungeon_World', 'http://buddyfight.wikia.com/wiki/Hero_World',
             'http://buddyfight.wikia.com/wiki/Katana_World', 'http://buddyfight.wikia.com/wiki/Legend_World',
             'http://buddyfight.wikia.com/wiki/Magic_World', 'http://buddyfight.wikia.com/wiki/Star_Dragon_World',
             'http://buddyfight.wikia.com/wiki/Monster', 'http://buddyfight.wikia.com/wiki/Flag',
             'http://buddyfight.wikia.com/wiki/Spell', 'http://buddyfight.wikia.com/wiki/Impact',
             'http://buddyfight.wikia.com/wiki/Item', 'http://buddyfight.wikia.com/wiki/SetList:BFE-H-BT04?action=edit', '']
    for i in range(0, len(links)):
        link1 = linkf(str(links[i]))
        if link1 not in bad_l:
            l.append(link1)
    return l        
