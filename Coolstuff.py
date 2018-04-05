#improved scraper for coolstuffinc
from w_csv import *
from Sel_session import *
from Im_dwnld import *
from con_text import *
from fn_grab import *
from S_format import *
import time
import re
import copy
import sys
class Coolstuff:
	def __init__(self, url):
		self.url = url
		self.dir = ''
		self.scrapeData = []
		self.h_var = False
		self.Dmvar = False

	def main_auto(self):
		url = self.url
		site = Sel_session(url, driver = 'C:\\Program Files\\Mozilla FirefoxSel\\firefox.exe')
		site.start()
		results = []
		dmDiceOnly = []
		dmNlst = []
		results_final = [["Product Name", "Rarity", "", "", "Product Image", "Affiliation","Card Text", "Card Type", "Casting Cost","Die Limit"]]
		if site.element_check('nextLink'):
			results.extend(self.images_desc(site.source()))
			site.js('window.scrollTo(0,document.body.scrollHeight);')
			time.sleep(5)
			while site.element_check('nextLink'):

				site.js("document.getElementById('nextLink').children[0].click();")
				try:
					time.sleep(5)
				except KeyboardInterrupt as KE:
					break
				site.js('window.scrollTo(0,document.body.scrollHeight);')
				time.sleep(5)
				results.extend(self.images_desc(site.source()))
		else:
			site.js('window.scrollTo(0,document.body.scrollHeight);')
			time.sleep(5)
			results.extend(self.images_desc(site.source()))
		if results != []:
			#loop grabs the image URLS
			#d_links = [results[i][1] for i in range(0, len(results))]
			for i in results:
				try:
					print(i)
				except UnicodeEncodeError as UE:
					print("Unicode Error, proceeding with image downloads")
			d_links = [re.sub('/c_pad,h_1\d\d,w_1\d\d', '', results[i][3]) for i in range(0, len(results))]
			#downloads the images
			Im_dwnld(self.dir).i_main(d_links)

		if self.Dmvar:
			#name = results[0][0].split(' - ')[0]
			#dmNlst.append(name)

			for i in range(0, len(results)-1):
				name = results[i][0].split(' - ')[0]
				if name not in dmNlst and "Basic Action Card" not in results[i][0]:
					print("{0} not in list".format(name))
					new_name = name + " (Die Only)"
					new_row = results[i][:]
					new_row[0] = new_name
					new_row[4] = "dicemasters.jpg"
					dmDiceOnly.append(new_row)
					dmNlst.append(name)
				#name = results[i+1][0].split(' - ')[0]
			r1 = copy.deepcopy(results)
			results_final.extend(self.DmVariants(" (Card Only)", r1))
			results_final.extend(self.DmVariants(" (Die and Card Combo)", r1))


			results_final.extend(dmDiceOnly)
			results = results_final


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
				if self.Dmvar:
					results.append(self.splitterDM(rows[i]))
				else:
					results.append(self.splitter(rows[i]))
			except RuntimeError as RE:
				results.append(["N/A"])
		return results
	def splitterDM(self, x):
		#takes bsobject and returns the picture, item name and number
		item = x
		image_r = item.find('td', {'class':'vm picture'})
		image_info = self.splitter_images(image_r)
		name = con_text_s(item.find('td', {'class':'vm description'}).find('span',{'itemprop':'name'}))
		item.find('td', {'class':'vm description'}).find('span',{'itemprop':'name'}).decompose()
		rarity = con_text_s(item.find('td', {'class':'vm description'}).find('h3'))
		rarity = rarity.replace(', ', '')
		rarity = rarity.strip(' ')
		results = [name, rarity] + image_info
		return results
	def DmVariants(self, x, lst):
		lst1 = copy.deepcopy(lst)
		for i in lst1:
			i[0] = i[0] + x
		return lst1



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

		if S_format(str(item)).linkf('src=') == 'https://res.cloudinary.com/csicdn/image/upload/v1/Images/fast_image.gif':
			link_i = S_format(str(item)).linkf('data-src=')
			link_i = re.sub("/c_pad,h_100,w_100", '', link_i)
			results = [S_format(str(item)).linkf('<img alt='),link_i, fn_grab(link_i)]
			return results

		else:
			link_i = S_format(str(item)).linkf('src=')
			link_i = re.sub("/c_pad,h_100,w_100", '', link_i)
			results = [S_format(str(item)).linkf('<img alt='),link_i, fn_grab(link_i)]
			return results




if __name__ == "__main__":
	if sys.argv[1] == '-hc':
		test = Coolstuff(sys.argv[2])
		test.dir = sys.argv[3]
		test.h_var = True
		test.main_auto()
	elif sys.argv[1] == '-dm':
		test = Coolstuff(sys.argv[2])
		test.dir = sys.argv[3]
		test.Dmvar = True
		test.main_auto()

	else:
		test = Coolstuff(sys.argv[1])
		test.dir = sys.argv[2]
		test.main_auto()
