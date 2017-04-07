#role4initiatve 
from soupclass8 import *

def splitter(x):
	site = S_base(x).soupmaker()
	prod_name = site.find('div', {'class':'myBoxHeader'}).text
	image = site.find('img', {"class":"image_frame float_l"})
	image_link  = "http://role4initiative.com" + S_format(str(image)).linkf('src=',0, 1)
	table = site.find('div', {'class':'myBoxContent h500'}).find('table')
	rows = table.find_all('tr')
	return table_process(table, prod_name, image_link)
def table_process(x, prod_name, image = 'N/A'):
	#takes bsObject as parameter
	rows = x.find_all('tr')
	results = []
	for i in range(1, len(rows)):
		cells = rows[i].find_all('td')
		new = []
		for i_2 in range(0, len(cells)):
			if i_2 != 3:
				new.append(cells[i_2].text)
		new.insert(0, prod_name)
		new.insert(1, image)
		new.insert(1, fn_grab(image))
		results.append(new)
	return results
def link_grab(x):
	#returns all the links in the search results page
	site = S_base(x).soupmaker()
	m_site = site.find("div", {"class":"cbox_fws"})
	link_elements = m_site.find_all("div", {'class':'myBoxHeader'})
	results = []
	for i in link_elements:
		raw_link = i.find('a')
		link = S_format(str(raw_link)).linkf('href=',0, 1)
		results.append(link)
	return results
def batch(x):
	#takes search result URLs and runs the links through the splitter function
	links = link_grab(x)
	results = []
	for i in links:
		print("Now processing {0}".format(i))
		i = i.replace(';','&')
		info = splitter(i)
		results += info
	return results

def batch_list(x):
	results = []
	for i in x:
		results += batch(i)
	return results




#h = splitter("http://role4initiative.com/search.php?pi=100&oos=oos&q=50001")
#test = link_grab("http://role4initiative.com/search.php?pi=50")
#batch_test = batch("http://role4initiative.com/search.php?pi=50")
batches = batch_list(['http://role4initiative.com/search.php?pi=41', 'http://role4initiative.com/search.php?pi=45', 'http://role4initiative.com/search.php?pi=44' ])
w_csv(batches, "r4i.csv")