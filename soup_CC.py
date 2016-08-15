#scraping collectors cache
from soupclass8 import *
from Im_dwnld import *
import sys
import re

#http://old.collectorscache.com/StoreModules/ShowCategory.aspx?CategoryID=189&tabid=9&tabindex=0&Show=All
def main_imp(x, start=0):
	urls = r_csv(x)
	try:
		int(start)
	except ValueError as VE:
		print('Second Argument must be a number')
		return
	for i in range(int(start), len(urls)):
		fname = urls[i][0] + ".csv"
		main(urls[i][1], fname , urls[i][0].strip(' '))
	return "Complete"

def main(x, fname = 'jpokemon.csv', dir_name='Batch Test'):
	links = link_grab(x)
	new = [splitter(links[i]) for i in range(0, len(links))]
	w_csv(new, fname)
	new2 = [new[i][2] for i in range(0, len(new))]
	Im_dwnld(dir_name).i_main(new2)

def splitter(x):
	#scrapes the unique item page
	try:
		site = S_base(x).soupmaker()
	except: #try again
		site = S_base(x).soupmaker()
	if site.find('div', {'id':'ProductImagePane'}).find('img') != None:
		link = 'http://old.collectorscache.com/StoreModules/' + S_format(str(site.find('div', {'id':'ProductImagePane'}).img)).linkf('src=')
		name =  S_format(str(site.find('div', {'id':'ProductImagePane'}).img)).linkf('title=')
		return (name, fn_grab(link), link)
	else:
		return ("Nothing found for %s") % (x)

def link_grab(x):
	print("Scraping from %s" % (x))
	site = S_base(re.sub("&amp;tabid=9&amp;tabindex=0", "&tabid=&tabindex=&Show=All", x)).soupmaker() #should fix most from the list but will not work if scraped directly from site
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
	elif sys.argv[1] == '-csv':
		main_imp(sys.argv[2],sys.argv[3])
	else:
		print("[test] [url]")
		print("[-m/-csv] [url / file name] [output file name] [output directory for images]")


