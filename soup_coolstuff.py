from soupclass8 import *
from Im_dwnld import *
import sys

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
		results.extend(images_ng(site.source()))
		while site.element_check('nextLink'):
			site.js("document.getElementById('nextLink').children[0].click();")
			results.extend(images_ng(site.source()))
	if results != []:
		#loop grabs the image URLS
		d_links = [results[i][1] for i in range(0, len(results))]
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



if len(sys.argv) != 1:
	if sys.argv[1] == '-a':

		main_auto(sys.argv[2], sys.argv[3])
	

	else:
		main(sys.argv[1])
else:
	print("[file name]")

