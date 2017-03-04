from soupclass8 import *
from Im_dwnld import *

class Magic_release:
	def __init__(self, url, n_dir):
		self.url = url
		self.bsObject = S_base(url).soupmaker()
		self.crit = ["Name", "Image Link", "Product Image", "Color"]
		self.n_dir = n_dir
	def grab_cards(self, images=0):
		results = [["Product Name", "Image Link", "Product Image", "Color"]]
		self.bsObject.find_all('div', {'class':'resizing-cig'})
		white_sect = self.bsObject.find('div', {'id':'divwhite'})
		blue_sect = self.bsObject.find('div', {'id':'divblue'})
		black_sect = self.bsObject.find('div', {'id':'divblack'})
		red_sect = self.bsObject.find('div', {'id':'divred'})
		green_sect = self.bsObject.find('div', {'id':'divgreen'})
		mc_sect = self.bsObject.find('div', {'id':'divmulticolored'})
		art_sect = self.bsObject.find('div', {'id':'divartifact'})
		land_sect = self.bsObject.find('div', {'id':'divland'})
		blues = self.splitter(blue_sect, "Blue")
		whites = self.splitter(white_sect, "White")
		blacks = self.splitter(black_sect, "Black")
		reds = self.splitter(red_sect, "Red")
		greens = self.splitter(green_sect, "Green")
		mcs = self.splitter(mc_sect, "Multi-Colored")
		arts = self.splitter(art_sect, "Artifact")
		lands = self.splitter(land_sect, "Land")
		cards = [whites, blues, blacks, reds, greens, mcs, arts, lands]
		for i in range(0, len(cards)):
			results.extend(cards[i])
		if images != 0:
			image_urls = [results[i][1] for i in range(1, len(results))]
			Im_dwnld(self.n_dir).i_main(image_urls)
		w_csv(results, "New_m_set.csv")

		return results










	def splitter(self, x, color):
		items = x.find_all('div', {'class':'resizing-cig'})
		results = []
		for i in range(0, len(items)):
			d = {}
			d["Name"] = re.sub('\n', '', items[i].text)
			d["Image Link"] =  S_format(str(items[i].img)).linkf('src=')
			d["Product Image"] = fn_grab(d["Image Link"])
			d["Color"] = color
			results.append(S_format(d).d_sort(self.crit))
		return results




test = Magic_release('http://magic.wizards.com/en/articles/archive/card-image-gallery/modern-masters-2017-edition', "Modern Masters")
res = test.grab_cards()