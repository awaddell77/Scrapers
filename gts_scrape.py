from soupclass8 import *
from GtsSelect import *
#for gts scraping

import sys
def main_s(x):
    #site = S_base(x,'ul','class', 'detail_info')
    #full_site = site.soupmaker()
    full_site = S_base(x).soupmaker()
    need_list = ['Product Name:', 'Sku', 'UPC each:', 'Barcode:', 'Release Date:', 'Manufacturer:', 'Product Image:', 'Image Link:', 'Category:', 'Catalog Category']


    return S_format(dict_sort(gts_split(full_site))).d_sort(need_list)

def main_batch1(x):#links must be pre-scraped and saved in a text file
    need_list = ['Product Name', 'Sku', 'UPC each:', 'Release Date:', 'Manufacturer:', 'Product Image:', 'Image Link:','Category:','Catalog Category']
    results = [['Product Name', 'Sku', 'UPC each:', 'Release Date:', 'Manufacturer:', 'Product Image:', 'Image Link:','Category:']]
    if type(x) == str:
        all_links = S_IO(x).text_l()
    elif type(x) == list:
        all_links = x
    else:
        return "Argument must be either string or list"
    print('%d link(s) detected.' % (len(all_links)))
    count = 0
    for i in range(0 ,len(all_links)):
        h = main_s(all_links[i])
        try:
            print(h)
        except UnicodeEncodeError as UE:
            print("Encountered unicode error. Proceeding with scrape.")
        print(all_links[i])
        results.append(main_s(all_links[i]))
        print('%s completed!' % (all_links[i]))
        count = count + 1
        print('That was number  %d, next is number %d' % (count, count + 1))
    #w_csv(results)
    print("Completed. Output contains %s items." % (len(results)))
    return results

def main_batch2(x):#same as main_batch1 except it does not call main_s and instead does the job of main_s by itself
    need_list = ['Product Name:', 'Sku', 'UPC each:', 'Barcode:', 'Release Date:', 'Manufacturer:', 'Product Image:', 'Image Link:']
    results = [['Product Name', 'Sku', 'UPC each:', 'Release Date:', 'Manufacturer:', 'Product Image:', 'Image Link:']]
    all_links = S_IO(x).text_l()
    print('%d link(s) detected.' % (len(all_links)))
    count = 0
    for i in range(0 ,len(all_links)):
        site = S_base(all_links[i],'ul','class', 'detail_info')
        full_site = site.soupmaker()
        results.append(S_format(dict_sort(gts_split(full_site))).d_sort(need_list))
        print('%s completed!' % (all_links[i]))
        count = count + 1
        print('That was number  %d, next is number %d' % (count, count + 1))
    w_csv(results)
    return "Completed. Output contains %s items." % (len(results))



def gts_split(x):
    l = []
    d = {'Product Name:':''}
    picture_info = pict_finder(x)#gets image information
    d['Image Link:'] = picture_info[0]
    d['Product Image:']= picture_info[1]
    contents_head = x.find('div', {'id':'detail_wrap'})
    d['Product Name:'] = cleaner(contents_head.h1.text, ["\n", "\t", "\r"])
    table = x.find('ul', {'class', 'detail_info'})
    contents = table.find_all('li')
    for i in range(0, len(contents)):
        if contents[i].span != None:
            d[(cleaner(contents[i].span.text, ["\n", "\t", "\r"]))] = cleaner(contents[i].text,["\n", "\t", "\r", "\xa0", "&nbsp;"])

    return d

def dict_sort(x):#parses values in order to make them readable
    keys = list(x.keys())
    values = list(x.values())
    n_keys = []
    n_values = []
    d2 = x
    no_sort = ['Product Name:','Product Image:', 'Image Link:',"Catalog Category"]
    need_list = ['Sku', 'UPC each:', 'Release Date:', 'Manufacturer:', 'Product Image:', 'Image Link:']
    for i in range(0, len(d2.keys())):
        if ':' in d2[keys[i]] and keys[i] not in no_sort:
            d2[keys[i]] = d2[keys[i]].split(':')[1].strip(' ')
        elif ':' not in keys[i] and keys[i] not in no_sort:#changed
            d2[keys[i]] = d2[keys[i]].split(' ')[1].strip(' ')
    if d2.get('UPC each:','N/A') == 'N/A':
        if d2.get('Barcode:', 'N/A') == 'N/A':
            d2['UPC each:'] = 'N/A'
        elif d2.get('Barcode:', 'N/A') != 'N/A':
            d2['UPC each:'] = "'" + d2['Barcode:']
        else:
            d2['UPC each:'] = 'N/A'
    catCategory = GtsSelect(d2["Product Name:"], d2.get("Manufacturer:", 'N/A'))
    catCategory.select(d2["Category:"])
    d2["Catalog Category"] = catCategory.category

    d2['UPC each:'] = "'" + d2['UPC each:']
    return d2

def pict_finder(x):
    print(type(x))
    site = x.find('div', {'id':'product-container-main'})
    try:
        picture = site.find('a')
    except AttributeError as AE:
        return ["No Picture Found", "No Picture Found"]
    if picture == None:
        return ["No Picture Found", "No Picture Found"]
    picture_link = [ S_format(str(picture)).linkf('href=','http://www.gtsdistribution.com/')]
    picture_name = picture_link[0].split('/')
    #print(picture)
    picture_link.append(picture_name[len(picture_name)-1])#file name
    return picture_link

def links(x):
    links_1 = S_IO(x).text_l()#opens text file containing links to link tables
    link_list = []
    for i in range(0, len(links_1)):
        page = S_base(links_1[i], 'table', 'id', 'list_layout')
        table = page.soup_target()
        links_all = table.find_all('a')
        for i_2 in range(0, len(links_all)):
            new = S_format(str(links_all[i_2])).linkf('<a href=')
            if new != None:
                link_list.append(new)
    link_list = dupe_erase(link_list)
    text_wc(link_list)
    return link_list

def links_1(x):
    if 'http://' in x:
        links_1 = [x]
    else:
        links_1 = S_IO(x).text_l()
    link_list = []
    for i in range(0, len(links_1)):
        page = S_base(links_1[i], 'table', 'id', 'list_layout')
        table = page.soup_target()
        links_all = table.find_all('a')
        for i_2 in range(0, len(links_all)):
            new = S_format(str(links_all[i_2])).linkf('<a href=')
            if new != 'None':
                if "http://www.gtsdistribution.com/" not in new:
                    new = "http://www.gtsdistribution.com/" + new
                    link_list.append(new)
                else:
                    link_list.append(new)
    link_list = dupe_erase(link_list)
    text_wc(link_list)
    return link_list
if len(sys.argv) > 1:
    if sys.argv[1] == '-l': #lower case L
        results = main_batch1(links_1(sys.argv[2]))
        w_csv(results, 'gts-pos.csv')
    elif sys.argv[1] == '-t':
        main_batch1(sys.argv[2])
else:
    print("[Website containing links]")
