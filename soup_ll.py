#for scraping Luck and Logic Singles from http://en.luck-and-logic.com/cardlist/list/BT01/
from soupclass8 import *

def ll_main(x):
	urls = text_l(x)
	results = [['NAME', 'ATTRIBUTE 1', 'ATTRIBUTE 2', 'CARD NO.', 'PARADOX RULE', 'POWER', 'AURA', 'INTERCEPT', 'RARITY', 'SOUL', 'TERRITORY', 'LEVEL', 'TYPE', 'LOGIC',
	 'WORLD', 'GATE NUMBER', 'COLOR', 'COST', 'TEXT', 'LIMIT', 'COVENANTER']]
	for i in range(0, len(urls)):
		results.append(splitter(urls[i]))
	w_csv(results,'C:\\Users\\Owner\\LLFILE.csv')
	return results


def splitter(x):
	site = S_base(x).soupmaker()
	table = site.find('div', {'class':'card-detail'})
	headers = table.find_all('th')
	crit = ['NAME', 'ATTRIBUTE 1', 'ATTRIBUTE 2', 'CARD NO.', 'PARADOX RULE', 'POWER', 'AURA', 'INTERCEPT', 'RARITY', 'SOUL', 'TERRITORY', 'LEVEL', 'TYPE', 'LOGIC',
	 'WORLD', 'GATE NUMBER', 'COLOR', 'COST', 'TEXT', 'LIMIT', 'COVENANTER']
	d={}
	d['NAME'] = headers[0].text #the title
	for i in range(1, len(headers)):
		cell = headers[i].find_next_sibling()
		if headers[i].text == 'COLOR' or headers[i].text == 'WORLD':
			d[headers[i].text] = fn_grab(S_format(str(cell.img)).linkf('<img src='))
		elif headers[i].text == 'AURA' or headers[i].text == 'TERRITORY':
			d[headers[i].text] = S_format(str(cell.img)).linkf('<img alt=')

		else:
			d[headers[i].text] = cell.text

	return S_format(d).d_sort(crit)

def i_n_splitter(x): #grabs image link and card name from main card table
	site = S_base(x).soupmaker()
	cards = site.find('ul', {'class':'card-single-list'})
	items = cards.find_all('li')
	results = []
	for i in range(0, len(items)):
		image_link = 'http://en.luck-and-logic.com' + S_format(str(items[i].img)).linkf('<img src=')
		link = 'http://en.luck-and-logic.com' + S_format(str(items[i].find('a'))).linkf('href=')
		image_name = fn_grab(image_link)
		rows = items[i].find_all('tr') #all of the rows
		name = rows[0].th.text
		number = rows[1].td.text
		results.append((name, number, link, image_name, image_link))
	return results






