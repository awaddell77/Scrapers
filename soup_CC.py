#scraping collectors cache
from soupclass8 import *
import sys

def splitter(x):
	#scrapes the unique item page
	site = S_base(x).soupmaker()
	if site.find('div', {'id':'ProductImagePane'}).find('img') != None:
		link = 'http://old.collectorscache.com/StoreModules/' + S_format(str(site.find('div', {'id':'ProductImagePane'}).img)).linkf('src=')
		name =  S_format(str(site.find('div', {'id':'ProductImagePane'}).img)).linkf('title=')
		return (name, link)
	else:
		return ("Nothing found for %s") % (x)

def link_grab(x):
	site = S_base(x +'&Show=All').soupmaker()
	links_r = site.find_all('li', {'class':'productInfo'})
	new = ['http://old.collectorscache.com/StoreModules/' + S_format(str(links_r[i].a)).linkf('<a href=') for i in range(0, len(links_r))]
	return new



if len(sys.argv) != 1:
	if sys.argv[1] == 'test':
		print("Processing %s" % sys.argv[2])
		print(splitter(sys.argv[2]))
	else:
		print("[test] [url]")


