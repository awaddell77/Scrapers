#desunation
from soupclass8 import *

class D_nation:
	def __init__(self):
		self.__url = ''
		self.__links = []
		self.__cards = []
		self.browser = ''

	def get_url(self):
		return self.__url
	def set_url(self, x):
		self.__url = x
	def get_links(self):
		return self.__links
	def set_links(self, x):
		self.__links = x
	def get_cards(self):
		return self.__cards
	def set_cards(self, x):
		self.__cards = x
	def get_names(self):
		site = self.browser.source()
		table = site.find("div", {'class':'products-container browse'})
		rows = table.find_all('h4', {'class':'name'})
		for i in rows:
			card_name = cleaner(i.text, ["\n", "\r", "\t"])
			self.__cards.append([uni_clean(card_name)])
	def scrape_names(self):
		self.browser = Sel_session(self.get_url())
		self.browser.start()
		time.sleep(1)
		self.browser.w_load()
		while True:
			if not self.browser.js("return document.getElementsByClassName('next_page')[0]"):
				self.get_names()
				break
			else:
				self.get_names()
				self.browser.js("document.getElementsByClassName('next_page')[0].click()")
				self.browser.w_load()
		self.browser.close()
		return self.get_cards()

	def scrape_links(self):
		#scrapes single page using url data field
		self.browser = Sel_session(self.get_url())
		self.browser.start()
		site = self.browser.source()
		table = site.find("div", {'class':'products-container browse'})
		card_links_r = site.find_all('div', {"class":"meta"})
		card_links = [S_format(str(i)).linkf('href=', "http://www.desunation.com", 1) for i in card_links_r]
		links += card_links		
	def scrape_product_info(self):
		pass
	def scrape_product_info_single(self, x):
		d = {}
		self.browser.go_to(x)
		site = self.browser.source()
		prod_desc = site.find('div', {'itemprop':'description'})
		d["Product Name"] = cleaner(prod_desc.find('h1', {'class':'title'}).text, ["\n", "\r", "\t"])
		pass




if __name__ == "__main__":
	if sys.argv[1] == '-names':
		d_inst = D_nation()
		d_inst.set_url(sys.argv[2])
		d_inst.scrape_names()
		cards = d_inst.get_cards()
		w_csv(cards, "desu-cards.csv")

