#http://mlpccg.wikia.com/wiki/Scootaloo,_Cutie_Mark_Crusader
from soupclass8 import *

def mlp_main(x):
	urls = text_l(x)
	results = []
	for i in range(0, len(urls)):
		results.append(splitter(urls[i]))
	w_csv(results)
	return results



def splitter(x):
	site = S_base(x).soupmaker()
	table = site.find('div', {'id':'mw-content-text'}).table.table
	rows = table.find_all('tr')
	crit = ['Name', 'Card Type', 'Color', 'Traits', 'Game Text', 'Power', 'Image Link', 'Image']
	d = {}
	d['Name'] = site.find('div',{'class':'header-container'}).h1.text
	d["Image Link"] = S_format(str(site.find('div', {'id':'mw-content-text'}).p.img)).linkf('src=')
	d["Image"] = S_format(str(site.find('div', {'id':'mw-content-text'}).p.img)).linkf('data-image-key=')
	for i in range(0, len(rows)):
		cells = rows[i].find_all('td')
		if len(cells) == 2:
			if d.get(cells[0].text, 'None found') != 'None found':
				d[cells[0].text] = d[cells[0].text] + ' // ' + cleaner(cells[1].text, '\n')
			else:
				d[cells[0].text] = cleaner(cells[1].text,'\n')
	return S_format(d).d_sort(crit)







