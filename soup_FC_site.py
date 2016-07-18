#for scraping information from the FCBF website (http://fc-buddyfight.com/en/cardlist/list/?id=36)
from soupclass7 import *
crit = ['Name', 'Power', 'Card Type', 'Attribute', 'Expansion', 'Card No.', 'Defense', 'Ability/Effect', 'Critical', 'World', 'Rarity', 'Size']

def main(x):
	urls = text_l(x)
	results = []
	for i in range(0, len(urls)):
		results.append(splitter(urls[i]))
	return results

def splitter(x):
	d = {}
	site = S_base(x).soupmaker()
	table = site.find('table',{'class':'common-table status'})
	rows = table.find_all('tr')
	name =  S_format(site.find('p', {'class':'card_name'}).text).encoder()
	#name and rarity are not included in d in order to make parsing easier
	rarity = S_format(str(site.find('p', {'class':'rare'}).img)).linkf('<img alt=')

	for i in range(0, len(rows)):
		headers = rows[i].find_all('th')
		for i_2 in range(0, len(headers)):
			d[headers[i_2].text] = headers[i_2].find_next()
			if d[headers[i_2].text] != None and headers[i_2].text != 'Illustrator':
				d[headers[i_2].text] = S_format(d[headers[i_2].text].text).encoder()
	d['Name'] = name
	d['Rarity'] = rarity
	return S_format(d).d_sort(crit)


#def format(x):
	#accepts dictionary (x) and changes their values into text



