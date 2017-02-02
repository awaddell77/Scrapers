from soupclass8 import *

def splitter(x, name):
	site = S_base(x).sel_soup()
	table = S_table(site)
	a_table = table.table_find_str(name)
	rows = a_table.find_all('tr')
	results= [['Number', 'Name', 'Rarity']]
	for i in range(0, len(rows)):
		new = []
		cells = rows[i].find_all('td')
		for i_2 in range(0, len(cells)):
			if i_2 == 1:
				link = "http://web.archive.org" + S_format(str(cells[i].find('a'))).linkf('href=')
				text = cells[i].find('td').text
				new.append(link)
				new.append(text)
			else:
				text = cells.find('td').text
				new.append('text')
		results.append(new)
	return results


