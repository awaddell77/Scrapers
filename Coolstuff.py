#improved scraper for coolstuffinc
from w_csv import *
from Sel_session import *
from Im_dwnld import *
from con_text import *
from fn_grab import *
from S_format import *
import time
import re
class Coolstuff:
	def __init__(self, url):
		self.url = url
		self.dir = ''
		self.scrapeData = []
		self.h_var = False

	def main_auto(self):
		url = self.url
		site = Sel_session(url)
		site.start()
		results = []
		if site.element_check('nextLink'):
			results.extend(self.images_desc(site.source()))
			while site.element_check('nextLink'):

				site.js("document.getElementById('nextLink').children[0].click();")
				try:
					time.sleep(5)
				except KeyboardInterrupt as KE:
					break
				results.extend(self.images_desc(site.source()))
		else:
			results.extend(self.images_desc(site.source()))
		if results != []:
			#loop grabs the image URLS
			#d_links = [results[i][1] for i in range(0, len(results))]
			for i in results:
				print(i)
			d_links = [re.sub('/c_pad,h_1\d\d,w_1\d\d', '', results[i][3]) for i in range(0, len(results))]
			#downloads the images
			Im_dwnld(self.dir).i_main(d_links)

				

		w_csv(results)
		site.close()
		self.scrapeData = [results,d_links]

	def images_desc(self, x):
		if isinstance(x, bs):
			site = x
		else:
			raise TypeError("Argument needs to be either a string or a beautiful soup object")
		results = []
		table = site.find('table', {'class':'vt mySearch'})
		rows = table.find_all('tr', {'itemtype':'http://schema.org/Product'})
		for i in range(0, len(rows)):
			try:
				results.append(self.splitter(rows[i]))
			except RuntimeError as RE:
				results.append(["N/A"])
		return results
	def splitter(self, x):
		#takes bsobject and returns the picture, item name and number
		item = x
		image_r = item.find('td', {'class':'vm picture'})
		image_info = self.splitter_images(image_r)
		name = con_text_s(item.find('td', {'class':'vm description'}).find('h3'))
		number = re.sub('Notes: ', '', con_text_s(item.find('div', {'class':'sSec'}).find('p', {'class':'pNotes'})))
		if self.h_var:
			number = name.split(" - ")[0].split(',')[0]
			rarity = name.split(" - ")[0].split(',')[len(name.split(" - ")[0].split(','))-1]
			return [name, number, rarity, image_info]
		results = [name, number] + image_info
		return results


	def splitter_images(self, x):
		#takes the raw image element from 
		item = x.find('img', {'itemprop':'image'})
		results = []

		if S_format(str(item)).linkf('src=') == 'http://res.cloudinary.com/csicdn/image/upload/v1/Images/fast_image.gif':
			link_i = S_format(str(item)).linkf('data-src=')
			link_i = re.sub("/c_pad,h_100,w_100", '', link_i)
			results = [S_format(str(item)).linkf('<img alt='),link_i, fn_grab(link_i)]
			return results

		else:
			link_i = S_format(str(item)).linkf('src=')
			link_i = re.sub("/c_pad,h_100,w_100", '', link_i)
			results = [S_format(str(item)).linkf('<img alt='),link_i, fn_grab(link_i)]
			return results





test = Coolstuff("http://www.coolstuffinc.com/page/3652&resultsperpage=25&sb=&sh=1")
test.dir = "Images"
test.main_auto()