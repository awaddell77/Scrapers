import lxml, requests
from bs4 import BeautifulSoup as bs
import csv
from soupclass8 import *
 
'''NOTES: 2/10/2016
-
-Moved bsObject into main function in order to decrease redundant get requests
-Added thtd function which theoretically allows program to grab the cells of tables with the th-td configuration


4/27/16
-Removed extra functions


5/6/2016
-
'''

    


def main2(x):
    urls  = text_l(x)
    t_results = []
    for i in range(0, len(urls)):
        new = main_s(urls[i])
        t_results.extend(new)
    w_csv(t_results)
    return t_results


def main(x):#batch
    
    urls  = text_l(x)
    t_results = [['Clan','Trigger', 'Grade / Skill', 'Name', 'Power', '', '', 'Race', 'Nation', 'Critical', 'Shield', 'Card Effect', 'Set Name']]
    for i in range(0, len(urls)):
        bsObject = S_base(urls[i]).soupmaker_batch()
        
        image_link = 'None Available'
        if bsObject.find('div', {'style':'float:left;'}) != None:
            image_r = bsObject.find('div', {'style':'float:left;'}).a
            image_link = S_format(str(image_r)).linkf('href=')
            image = image_link.split('/')[7]

        a_table = sfind(bsObject)

        print('ATTEMPTING TO PROCESS %s' % (urls[i]))
        if a_table == None:
            n = 0
            while type(a_table) == None and n != 10:
                a_table = sfind(bsObject)
                n += 1

        elif len(a_table) == 2:
            b_rows = td(a_table[0])
            b_rows.append(re.sub('\n','', a_table[1].text))
            b_rows.append(image_link)
            b_rows.append(image)
            t_results.append(b_rows)
        else:
            b_rows = td(a_table)
            b_rows.append(image_link)
            b_rows.append(image)
            t_results.append(b_rows)


    w_csv(t_results)
    #print(t_results)
    print("Complete")
    return t_results

def main_s(x): #singles
    urls = [x]
    t_results = []
    for i in range(0, len(urls)):
        bsObject = soupmaker(urls[i])
        a_table = sfind(bsObject)
        print(a_table)
        if len(a_table) == 2:
            b_rows = td(a_table[0])
            b_rows.append(re.sub('\n','', a_table[1].text))
            t_results.append(b_rows)
        else:
            b_rows = td(a_table)
            t_results.append(b_rows)
    w_csv(none_remover(t_results))
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
    print("%d entries were not found." % (none_c))
        
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
    bsObject = x
    table = bsObject.find('div',{'class':'info-main'})
    table2 = bsObject.find('table', {'class':'effect'})
    if table2 == None:
        return table
    else:
        return table,table2

def sfind2(x):#returns the image link as well
    bsObject = x
    d = {}
    d['Table'] = bsObject.find('div',{'class':'info-main'})
    d['Table 2'] = bsObject.find('table', {'class':'effect'})
    d['Image Link'] = bsObject.find('div', {'style':'float:left;'}).a
    return d

    

def encoder(x):#takes text from bsObject tag(s) and converts into unicode-free strings
    h = x
    try:
        h = x.encode('ascii', 'ignore')
        #print 'Tried to encode' #for testing
    except UnicodeEncodeError as U:
        h = h.encode('utf-8', 'ignore')
        print('UTF-8')
        return h
    except AttributeError as E:
        print(E)
        return x
    else:
        h = x.encode('ascii', 'ignore')
        print('ASCII')
        return h



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
                d[re.sub('\n', '', table_c[i].text).strip(' ')] = re.sub('\n','',table_c[i + 1].text).strip(' ')
            except IndexError as IE:
                print(d)
                return d_sort(d)
                
    try:
        print(d)
    except UnicodeEncodeError as UE:
        print('Retrieval Successful')
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
            d[encoder(headers[i].text).translate(None, '\n')] = encoder(headers[i].next_sibling.text).translate(None, '\n')
        else:
            d[encoder(headers[i].text).translate(None, '\n')] = "None"
        #l.append(head,cel
    return d
        
        
    
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
    criteria = ['Clan', 'Trigger effect', 'Grade / Skill', 'Name', 'Power', 'Unit Type', 'Trigger Unit', 'Race', 'Nation', 'Critical', 'Shield']
    default = "Not Available"
    for i in range(0, len(criteria)):
        n_l.append([d.get(criteria[i], default)])
        #del d[criteria[i]]
    #l = d.keys()
    '''for i in range(0, len(l)):
        if len(l[i]) > 12:
            n_l.append(l[i])'''
    return n_l
    
def l_maker(x):#sorts through elements of a list to check if those elements are lists
    l = []
    for i in range(0, len(x)):
        if isinstance(x[i], list) != True:
            l.append([x[i]])
        else:
            l.append(x[i])
    return l
     
    
    
    
        
        
    
        
'''def text_l(x):
    words = ''
    l = []
    with open(x, 'r') as f:
        data = f.readlines()
        for line in data:
            words = line.split()
            print words
            l.extend(words)
        print l
        return l'''
'''def sort1(x):#sorts through list deletes elements with specific keywords
    keyword = ["Kanji"]
    for i in range(0, len(x)):
        for l in'''
        
        
        
'''def w_csv(x,output='FCfile.csv'):#accepts lists of other lists, spits out CSV file
    csv_out = open(output, 'wb')
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
    return l'''
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




def images(x):
    numbers = text_l(x)
    results = []
    new = ['http://cardfight.wikia.com/wiki/File:' + numbers[i] + '.png' for i in range(0, len(images))]
    for i in range(0, len(new)):
        site = S_base(new[i]).soupmaker()
        link = S_format(str(site.a)).linkf('src=')
        results.append(link)
    return results

def main_gallery(x):
	site = S_base(x).soupmaker()
	r_links = site.find_all('div', {'class':'lightbox-caption'})
	new = [(r_links[i].text, 'http://cardfight.wikia.com' + S_format(str(r_links[i].a)).linkf('<a href=')) for i in range(0, len(r_links))]
	#new will be a list of tuples containing the card number and then link to the card
	link_write(new)
	return new

def link_write(x):
	links = [x[i][1] for i in range(0, len(x))]
	text_wc(links)
	numbers = [(joiner(x[i][0].split(' ')[1:]), x[i][0].split(' ')[0]) for i in range(0, len(x))]
	w_csv(numbers, 'Numbers1.csv')
	return "Complete"

def joiner(x,s = ' '):#accepts a list then joins its elements together with empty spaces
	'''if s != ' ':
		s'''
	return s.join(x) 