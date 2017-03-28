#magic 
#srapes a set page http://gatherer.wizards.com/Pages/Search/Default.aspx?set=[%22Duel%20Decks:%20Mind%20vs.%20Might%22]
from soupclass8 import *
class Magic_scrape:
	def __init__(self, url):
		self.url = url
		self.session = Sel_session(url)
		self.session.start()
		self.cards = []
		self.headers = ["Name", "Card Type", "Pow / Tgh", "Card Text", "Rarity"]

	def page_scrape(self):
		site = self.session.source()
		card_table = site.find('table',{'class':'cardItemTable'})
		card_table_rows = card_table.find_all('tr', {'class':'cardItem evenItem'}) 
		card_table_rows.extend(card_table.find_all('tr', {'class':'cardItem oddItem'}))
		#card_info = [i.find('div', {'class':'cardInfo'}) for i in card_table_rows]
		for i in card_table_rows:
			self.cards.append(self.__card_info_get(i))
		#print(self.cards)
	def page_source(self):
		pass

	def __card_info_get(self, x):
		#takes the div class='cardInfo' element, returns dictionary with all the card values
		d = {}
		card_info = x.find('div', {'class':'cardInfo'})
		d["Name"] = re.sub('\n', '', card_info.find('span', {'class':'cardTitle'}).text)
		type_attack = card_info.find('span', {'class':'typeLine'}).text
		if re.search('\(\d/\d\)', type_attack) != None:
			t_a = re.search('\(\d/\d\)', type_attack)
			d["Pow / Tgh"] = re.sub('\n', '', t_a.group())
			d["Card Type"] = re.sub('\n', '', type_attack.replace(d["Pow / Tgh"], '')).strip(' ')
		else:
			d["Card Type"] = re.sub('\n', '', type_attack).strip(' ')
			d["Pow / Tgh"] = ''
		d["Card Text"] = re.sub('\n', ' ', card_info.find('div', {'class':'rulesText'}).text)
		rarity = S_format(str(x.find('td', {'class':'rightCol setVersions'}).find('div',{'class':'rightCol'}).img)).linkf('<img alt=')
		d["Rarity"] = self.rarity_find(rarity)
		return d
	def m_csv(self):
		results = []
		results.append(self.headers)
		for i in self.cards:
			card = []
			for i_2 in self.headers:
				card.append(i[i_2])
			results.append(card)
		w_csv(results, "magic_set.csv")
	def pict_trans(self,x):
		if x.find('img') == None:
			return x
		else:
			x.find('img')
	def rarity_find(self, x):
		rarities = ['Rare', 'Common', 'Uncommon', 'Mythic Rare']
		for i in rarities:
			res = re.search('\({0}\)'.format(i), x)
			if res != None:
				return i[0]
		return 'Rarity Not Found'



if __name__ == '__main__':
	mag_inst = Magic_scrape(sys.argv[1])
	mag_inst.page_scrape()
	mag_inst.m_csv()
	mag_inst.session.close()





