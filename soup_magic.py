from soupclass6 import *


def main_s(x):
    results = []
    img_list = []
    site = S_base(x,'table', 'class', 'cardDetails')
    table = site.soup_target()
    if table == None:
        return None
    cardinfo = table.find_all('div', {'class':'value'})
    for i in range(0, len(cardinfo)):
        if cardinfo[i].find('img') != None:
            images = cardinfo[i].find_all('img')
            for a in range(0, len(images)):             
                new1 = S_format(str(images[a])).linkf('alt=')
                img_list.append(new1)
            results.append(img_list)
            img_list = []
        new = S_format(cardinfo[i].text).encoder().translate(None, '\r''\n').strip(' ')
        results.append(new)
    return results

def main_batch(x):
    urls = x
    results = []
    for i in range(0, len(urls)):
        results.append(main_s(urls[i]))
    return results


def main_alt(x):
    results = []
    img_list = []
    site = S_base(x,'table', 'class', 'cardDetails')
    table = site.soup_target()
    if table == None:
        return None
    cardinfo = table.find_all('div', {'class':'value'})
