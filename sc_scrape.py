#starcity
from soupclass8 import *
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
			if card_link is not None and card_link != 'None':
				results.append(card_link)
		return results
	def man_link_process(self):
		results = []
		card_links = []
		for i in self.urls:
			card_links +=  self.link_scrape(i)
		for i in card_links:
			results.append(self.splitter(i))
		self.m_results = results
		return results









test = StarCity("testing")
res = test.splitter("http://sales.starcitygames.com/carddisplay.php?productids[]=1330940")
print(res)
t_url = "http://sales.starcitygames.com/search.php?substring=Amonkhet+Prerelease&go.x=0&go.y=0&go=GO&t_all=All&start_date=2010-01-29&end_date=2012-04-22&order_1=finish&limit=25&action=Show%2BDecks&card_qty%5B1%5D=1"
t_url1 = "http://sales.starcitygames.com//search.php?substring=Amonkhet+Prerelease&start=50"
#print(test.link_scrape(t_url))
test.urls = [t_url, t_url1]
print(test.man_link_process())
w_csv(test.m_)




