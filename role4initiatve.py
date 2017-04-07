#role4initiatve 
from soupclass8 import *

def splitter(x):
	site = S_base(x).soupmaker()
	prod_name = site.find('div', {'class':'myBoxHeader'}).text
	image = site.find('img', {"class":"image_frame float_l"})
	image_link  = S_format(str(image)).linkf('src=',0, 1)
	d["Image Link"] = image_link
	table = site.find('div', {'class':'myBoxContent h500'}).find('table')
	rows = table.find_all('tr')
	return table_process(table, prod_name)
def table_process(x, prod_name):
	#takes bsObject as parameter
	rows = x.find_all('tr')
	results = []
	for i in range(1, len(rows)):
		cells = rows[i].find_all('td')
		new = []
		for i_2 in range(0, len(cells)):
			new.append(cells[i_2])
		new.insert(0, prod_name)
		results.append(new)
	return results






h = splitter("http://role4initiative.com/search.php?pi=100&oos=oos&q=50001")