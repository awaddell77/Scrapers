#norse foundry scraper (http://norsefoundry.com/)
from soupclass8 import *
import sys

browser = Sel_session()

def main(x):
	urls = t_link_grab(x)
	results = []
	for i in range(0, len(urls)):
		new = splitter(urls[i])
		results.append(new)
	w_csv(results, 'DICE.csv')
	return results

def splitter(x):
	browser.go_to(x)
	site = browser.source()
	name = site.find('h1', {'itemprop':'name'})
	sku = site.find('span', {'class':'sku_wrapper'})


	image_r = site.find('img', {'class':'inner-thumb'})
	image_link = S_format(str(image_r)).linkf('src=')
	image = fn_grab(image_link)
	new = list(con_text((name, sku)))
	new.extend([image_link, image])
	return new



def t_link_grab(x):
	urls = text_l(x)
	results = []
	for i in range(0, len(urls)):
		site = S_base(urls[i]).sel_soup()
		products = site.find_all('div', {'class':'product'})
		links = [S_format(str(products[i_2].find('a'))).linkf('href=') for i_2 in range(0, len(products))]
		results.extend(links)
	return results

if len(sys.argv) > 1:
	main(sys.argv[1])
else:
	print('TEXT FILE')
