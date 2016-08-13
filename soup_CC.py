#scraping collectors cache
from soupclass8 import *
from Im_dwnld import *
import sys
import re

#http://old.collectorscache.com/StoreModules/ShowCategory.aspx?CategoryID=189&tabid=9&tabindex=0&Show=All

def main(x, fname = 'jpokemon.csv', dir_name='Batch Test'):
	links = link_grab(x)
	new = [splitter(links[i]) for i in range(0, len(links))]
	w_csv(new, fname)
	new2 = [new[i][1] for i in range(0, len(new))]
	Im_dwnld(dir_name).i_main(new2)

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
	print("Scraping from %s" % (x))
	site = S_base(x + 'Show=All').soupmaker()
	links_r = site.find_all('li', {'class':'productInfo'})
	new = ['http://old.collectorscache.com/StoreModules/' + re.sub('amp;','', S_format(str(links_r[i].a)).linkf('<a href=')) for i in range(0, len(links_r))]
	print(new)
	return new



if len(sys.argv) != 1:
	if sys.argv[1] == 'test':
		print("Processing %s" % sys.argv[2])
		print(splitter(sys.argv[2]))
	elif sys.argv[1] == 'test2':
		print(link_grab(sys.argv[2]))
	elif sys.argv[1] == '-m':
		main(sys.argv[2], sys.argv[3], sys.argv[4])
	else:
		print("[test] [url]")
		print("[-m] [url] [output file name] [output directory for images]")


