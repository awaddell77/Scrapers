
from soupclass7 import *
#troll and toad link grabber



def info_links(x):#grabs the links to products' individual pages
    site = S_base(x).soupmaker()
    links_r = site.find_all('div', {'class':'cat_result_text'})
    new = [S_format(str(links_r[i].a)).linkf('<a href=', 'http://www.trollandtoad.com') for i in range(0, len(links_r))]
    text_wc(new)
    return new
def main_info(x):
    urls = text_lc(x)
    results = [splitter(urls[i]) for i in range(0, len(urls))]
    w_csv(results, 'TNT1.csv')
    return results



def sorter(x):#takes bsObject grabs all the links
    l = []
    table = x.find('div', {'class':'catResults'})
    links = table.find_all('a')
    for i in range(0, len(links)):
        new = S_format(links[i].text).encoder().translate(None, '\n')#link title
        new1 = S_format(str(links[i])).linkf('<a href=')#link
        if new != None and new != ' ':
            l.append([new, new1])
    return dupe_erase(l)
        
def main_images(x):
    urls = text_lc(x)
    results = [['Card Name', 'Image', 'Image Link']]
    for i in range(0, len(urls)):
        results.extend(images(urls[i],1))
    w_csv(results,'TNT.csv')
    return results
def images(x,csv_out = 0, base='http://940ee6dce6677fa01d25-0f55c9129972ac85d6b1f4e703468e6b.r99.cf2.rackcdn.com/products/pictures/'):#can handle bsObjects and url strings
    site = x
    if type(x) == str:
        site = S_base(x).soupmaker()
    '''title = 'TROLL FILES'
    if site.find('div', {'class':'catResults'}).h1.text != None:
        title = S_format(site.find('div', {'class':'catResults'}).h1.text).encoder().translate(None, '\n''\r')'''#title feature will be added later
    links = site.find_all('div', {'class':'cat_result_image_wrapper'})
    #print(links)
    images = [links[i].img for i in range(0 , len(links))]
    #print(images)
    image_links = [(S_format(str(images[i])).linkf('<img alt='), fn_grab(S_format(str(images[i])).linkf('src=')), base + fn_grab(S_format(str(images[i])).linkf('src='))) for i in range(0, len(images))]#should return tuple of card name and image title
    if csv_out == 0:#by default the function writes the product and image file names as a csv file
        w_csv(image_links, 'TNT.csv')
    return image_links
    
def splitter(x):
    url = x
    site = S_base(url).soupmaker_batch()
    d= {}
    image_link_r = site.find('div', {'id':'product_image'}).img
    image_link = S_format(str(image_link_r)).linkf('src=')
    d['Image Link'] = image_link
    d['Product Image'] = 'None Found'
    if image_link != None:
        d['Product Image'] = fn_grab(image_link)
    p_name = site.find('h1', {'class':'product_name'}) #grabs the product name
    p_info = site.find('div', {'class':'details'}).find_all('tr')
    for i in range(0, len(p_info)):
        cells = p_info[i].find_all('td') #grabs all of the cells inside of the particular row
        if len(cells) == 2:
            d[spacesmash(cells[0].text)] = cells[1].text
    results = (p_name.text, d['Figure Number:'], d['Rarity:'], image_link, d['Product Image'])
    return results



        
        
