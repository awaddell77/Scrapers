from soupclass8 import *
#scrapes from bulbapedia



class Pkm_scrape:
	def __init__(self, url=''):
		self.url = url
		self.set_page = ''
		self.page_data = ''
		self.set_links = []
		self.card_info = []
	
	def clean_page(self, x):
		#creates bs object and removes unwanted elements from text
		#returns bs object
		site = S_base(x).soupmaker()
		new_site = str(site)
		new_site = new_site.replace('&nbsp;', '')
		new_site = new_site.replace('\n', '')
		new_site = bs(new_site, 'lxml')
		self.page_data = new_site
		return new_site
	def process_table(self, set_name):
		pass
	def get_card_data(self, x):
		d = {}
		site = self.clean_page(x)
		d["Stage"] = site.find(string=re.compile("Evolution")).parent.find_next('td')
		d["Name"] = site.find(string=re.compile(" Card name")).parent.find_next('td')
		d["Type"] = site.find(string=re.compile("Type")).parent.find_next('td')
		d["Hit Points"] = site.find(string=re.compile("Hit Points")).parent.find_next('td')
		d["Card Number"] = site.find(string=re.compile("English card no.")).parent.find_next('td')
		weakness_raw = site.find(string=re.compile("weakness")).parent.find_next('a').img
		if weakness_raw is not None:
			d["Weakness"] = S_format(str(weakness_raw)).linkf('<img alt=')
		else:
			d["Weakness"] = 'N/A'
		resistance_raw = site.find(string=re.compile("resistance")).parent.find_next('a').img
		if resistance_raw is not None:
			d["Resistance"] = S_format(str(resistance_raw)).linkf('<img alt=')
		else:
			d["Resistance"] = "N/A"

		rarity_raw = site.find(string=re.compile("Rarity")).parent.find_next('td').a
		if rarity_raw is not None:
			d["Rarity"] = S_format(str(rarity_raw)).linkf('title=')
		else:
			d["Rarity"] = "N/A"
		d_lst = list(d.keys())
		for i in d_lst:
			if i not in ["Rarity", "Weakness", "Resistance"]:
				d[i] = re.sub('\n', '', d[i].text.strip(' '))
		return d









