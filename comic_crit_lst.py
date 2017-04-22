#comic crit listing scraper
from soupclass8 import *

def scraper():
	url = 'https://retailer.diamondcomics.com/Home/1/1/28/905?articleID=26691'
	site = S_base(url).soupmaker()
	table = site.find("div",{'align':'center'}).table
	rows = table.find_all('tr')
	d = {}
	for i in range(1, len(rows)):
		cells = rows[i].find_all('td')
		count = 1
		crit_code = ''
		for i_2 in cells:
			if count % 2 == 0:
				value = i_2.text.replace('\n', '')
				value = value.replace('\u2013', '-')

				d[crit_code] = value
				count += 1
			elif i_2.text != '\n\xa0\n':
				crit_code = i_2.text.replace('\n', '')
				d[crit_code] = ''
				count += 1
	return d

