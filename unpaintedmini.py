#wizkids unpaintd mini 
from soupclass8 import *

browser = Sel_session()

def splitter(x):
	#takes table and scrapes info from it
	table = x
	rows = x.find_all('tr')
	results = []
	for i in range(1, len(rows)):
		name = rows[i].find('td', {'class': 'column-2'})
		sku = rows[i].find('td', {'class':'column-1'})
		image_r = rows[i].find('td', {'class':'column-3'}).find('img')
		image_link = S_format(str(image_r)).linkf('<img src=')
		image = fn_grab(image_link)
		new = list(con_text([name, sku]))
		new.extend([image_link, image])

		results.append(new)
	w_csv(results)
	return results

