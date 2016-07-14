
from soupclass8 import *

#pirate lab scraper (http://piratelab.com/)

def main(x):
	results = []
	urls = text_l(x)
	browser = webdriver.Firefox()
	for i in range(0, len(urls)):
		browser.get(urls[i])
		results.append(splitter(bs(browser.page_source,'lxml')))
	w_csv(results)
	browser.quit()
	return results





def splitter(x):
	#site = S_base(x).sel_soup()
	site = x
	image = 'None'
	image_link = 'None'
	title = site.find('h1', {'itemprop':'name'}).text
	sku = site.find('span', {'class':'variant-sku'}).text
	image_r = site.find('div', {'class':'flex-viewport'}).find('li',{'class':'featured flex-active-slide'}).a
	if image_r != None:
		image = fn_grab(S_format(str(image_r)).linkf('href=')).split('?')[0]
		image_link = S_format(str(image_r)).linkf('href=')

	return (title, sku, image, image_link)


