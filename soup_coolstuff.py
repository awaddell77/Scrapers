from soupclass8 import *
from Im_dwnld import *
import sys, time

#var for handling heroclix
h_var = False

def main(x):
	urls = text_l(x)
	results = []
	for i in range(0, len(urls)):
		results.extend(images_ng(urls[i]))
	w_csv(results)
	return results
def main_auto(x,directory="Images"):
	url = x
	site = Sel_session(url)
	site.start()
	results = []
	if site.element_check('nextLink'):
		results.extend(images_desc(site.source()))
		while site.element_check('nextLink'):

			site.js("document.getElementById('nextLink').children[0].click();")
			try:
				time.sleep(5)
			except KeyboardInterrupt as KE:
				break
			results.extend(images_desc(site.source()))
	else:
		results.extend(images_desc(site.source()))
	if results != []:
		#loop grabs the image URLS
		#d_links = [results[i][1] for i in range(0, len(results))]
		d_links = [re.sub('/c_pad,h_1\d\d,w_1\d\d', '', results[i][3]) for i in range(0, len(results))]
		#downloads the images
		Im_dwnld(directory).i_main(d_links)

			

	w_csv(results)
	site.close()
	return (results,d_links)

def images_ng(x):
	#returns the image links, image names, and product names
	try:
		x.body
		
	except AttributeError as AE:
		if type(x) == str:
			site = S_base(x).sel_soup(0)
		else:
			print("Argument needs to be either a string or a beautiful soup object")
			return
	else:
		site = x
	links_r = site.find_all('img', {'itemprop':'image'})
	results = []
	for i in range(0, len(links_r)):
		if S_format(str(links_r[i])).linkf('src=') == 'http://res.cloudinary.com/csicdn/image/upload/v1/Images/fast_image.gif':
			link_i = S_format(str(links_r[i])).linkf('data-src=')
			link_i = re.sub("/c_pad,h_100,w_100", '', link_i)
			results.append((S_format(str(links_r[i])).linkf('<img alt='),link_i, fn_grab(link_i)))

		else:
			link_i = S_format(str(links_r[i])).linkf('src=')
			link_i = re.sub("/c_pad,h_100,w_100", '', link_i)
			results.append((S_format(str(links_r[i])).linkf('<img alt='),link_i, fn_grab(link_i)))
	return results

def images_desc(x):
	try:
		x.body
		
	except AttributeError as AE:
		if type(x) == str:
			site = S_base(x).sel_soup(0)
		else:
			print("Argument needs to be either a string or a beautiful soup object")
			return
	else:
		site = x
	results = []
	table = site.find('table', {'class':'vt mySearch'})
	rows = table.find_all('tr', {'itemtype':'http://schema.org/Product'})
	for i in range(0, len(rows)):
		try:
			results.append(splitter(rows[i]))
		except:
			results.append(("N/A"))
	return results





def splitter(x):
	#takes bsobject and returns the picture, item name and number
	item = x
	image_r = item.find('td', {'class':'vm picture'})
	image_info = splitter_images(image_r)
	name = con_text_s(item.find('td', {'class':'vm description'}).find('h3'))
	number = re.sub('Notes: ', '', con_text_s(item.find('div', {'class':'sSec'}).find('p', {'class':'pNotes'})))
	if h_var:
		number = name.split(" - ")[0].split(',')[0]
		rarity = name.split(" - ")[0].split(',')[len(name.split(" - ")[0].split(','))-1]
		return (name, number, rarity, image_info) 
	results = (name, number) + image_info
	return results


def splitter_images(x):
	#takes the raw image element from 
	item = x.find('img', {'itemprop':'image'})
	results = []

	if S_format(str(item)).linkf('src=') == 'http://res.cloudinary.com/csicdn/image/upload/v1/Images/fast_image.gif':
		link_i = S_format(str(item)).linkf('data-src=')
		link_i = re.sub("/c_pad,h_100,w_100", '', link_i)
		results = (S_format(str(item)).linkf('<img alt='),link_i, fn_grab(link_i))
		return results

	else:
		link_i = S_format(str(item)).linkf('src=')
		link_i = re.sub("/c_pad,h_100,w_100", '', link_i)
		results = (S_format(str(item)).linkf('<img alt='),link_i, fn_grab(link_i))
		return results





if len(sys.argv) != 1:
	if sys.argv[1] == '-a':

		main_auto(sys.argv[2], sys.argv[3])
	elif sys.argv[1] == '-ah':
		h = True
		main_auto(sys.argv[2], sys.argv[3])
	

	else:
		main(sys.argv[1])
else:
	print("[file name]")

