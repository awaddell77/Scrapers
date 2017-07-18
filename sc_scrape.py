#starcity
from soupclass8 import *
import sys

class StarCity:
	def __init__(self, urls):
		self.urls = urls
		self.m_results = []

	def splitter(self, x):
		#need name and product image
		site = S_base(x).soupmaker()
		card_info = site.find('section', {"id":"content"})
		title = str(card_info.find('h2').text).replace('\n', '')
		#removing description so that program can get the images
		uc = card_info.find('div', {'class':'card_desc_details'})
		uc.decompose()
		image = card_info.find('img')
		image_link  = S_format(str(image)).linkf('src=')
		results = (title, fn_grab(image_link), image_link)
		return results
	def link_scrape(self, x):
		site = S_base(x).soupmaker()
		table = site.find("table", {'id':'search_results_table'})
		rows = table.find_all('tr')
		results = []
		for i in range(2, len(rows)):
			link = rows[i].find('td').find('a')
			card_link = S_format(str(link)).linkf("href=")
			if card_link is not None and card_link != 'None': results.append(card_link)
		return results
	def man_link_process(self):
		results = []
		card_links = []
		#needs to use checklist form for results on sc website
		for i in self.urls: card_links +=  self.link_scrape(i)
		for i in card_links: results.append(self.splitter(i))
		self.m_results = results
		return results







if __name__ == "__main__":
	test = StarCity(str(sys.argv[1]))
	print(sys.argv[0])
	print(sys.argv[1])
	urls = []
	for i in sys.argv[1:]: urls += [i]
	test.urls = urls
	w_csv(test.man_link_process())
