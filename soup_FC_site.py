#for scraping information from the FCBF website (http://fc-buddyfight.com/en/cardlist/list/?id=36)
from soupclass8 import *
import sys
crit = ['Name', 'Power', 'Card Type', 'Attribute', 'Expansion', 'Card No.', 'Defense', 'Ability/Effect', 'Critical', 'World', 'Rarity', 'Size']

def main(x):
	if type(x) == list:
		urls = x
	else:
		urls = text_l(x)
	results = [['Name', 'Power', 'Type', 'Attribute', 'Set Name', 'Card Number', 'Defense', 'Ability', 'Critical', 'World', 'Rarity', 'Size' ]]
	for i in range(0, len(urls)):
		results.append(splitter(urls[i]))
	w_csv(results)
	return results

def splitter(x):
	d = {}
	site = S_base(x).soupmaker()
	table = site.find('table',{'class':'common-table status'})
	rows = table.find_all('tr')
	name =  site.find('p', {'class':'card_name'}).text
	#name and rarity are not included in d in order to make parsing easier
	rarity = S_format(str(site.find('p', {'class':'rare'}).img)).linkf('<img alt=')

	for i in range(0, len(rows)):
		headers = rows[i].find_all('th')
		for i_2 in range(0, len(headers)):
			d[headers[i_2].text] = headers[i_2].find_next()
			if d[headers[i_2].text] != None and headers[i_2].text != 'Illustrator':
				d[headers[i_2].text] = d[headers[i_2].text].text
	d['Name'] = name
	d['Rarity'] = rarity
	return S_format(d).d_sort(crit)

def FC_site_link_scrape(x):
	#scrapes the links from the main site's card table
	url = x
	site = S_base(url).soupmaker()
	table = site.find('div', {'id':'cardList'})
	links_r = table.find_all('a', {'class':'ajax-popup-link'})
	new  = [S_format(str(links_r[i])).linkf('href=') for i in range(0, len(links_r))]
	return new

if len(sys.argv) > 1:
	main(FC_site_link_scrape(sys.argv[1]))
else:
	print("Link Name")
