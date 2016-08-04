from soupclass8 import *

def main(x):
	urls = text_l(x)
	results = []
	for i in range(0, len(urls)):
		results.extend(images_ng(urls[i]))
	w_csv(results)
	return results


def images_ng(x):
	#returns the image links, image names, and product names
	site = S_base(x).sel_soup(0)
	links_r = site.find_all('img', {'itemprop':'image'})
	results = []
	for i in range(0, len(links_r)):
		if S_format(str(links_r[i])).linkf('src=') == 'http://res.cloudinary.com/csicdn/image/upload/v1/Images/fast_image.gif':
			link_i = S_format(str(links_r[i])).linkf('data-src=')
			results.append((S_format(str(links_r[i])).linkf('<img alt='),link_i, fn_grab(link_i)))

		else:
			link_i = S_format(str(links_r[i])).linkf('src=')
			results.append((S_format(str(links_r[i])).linkf('<img alt='), link_i, fn_grab(link_i)))
	return results


