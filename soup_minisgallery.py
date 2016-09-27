#for scraping from minisgallery (http://www.minisgallery.com/dnd/dnd6.htm)
from soupclass8 import *
import sys



def splitter(x):
	site = S_base(x).sel_soup()
	elements = site.find_all('div',{'class':'miniframe'})
	results = []
	for i in range(0, len(elements)):
		rarity = elements[i].find('div', {'class':'boxrarity'})
		name = elements[i].find('div', {'class':'boxname_normal'})
		image_r = elements[i].find('div', {'class':'boximage'}).img
		image_link = S_format(str(image_r)).linkf('src=')
		image_name = fn_grab(image_link)
		new = con_text((name, rarity))
		results.append(new + (image_link, image_name))
	w_csv(results, "MINIS.csv")
	return results

if len(sys.argv) > 1:
	splitter(sys.argv[1])
else:
	print("URL")
