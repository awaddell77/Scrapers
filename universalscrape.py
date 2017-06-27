#for scraping from universaldist preorders (http://www.universaldist.com/pre-orders.aspx)
from soupclass8 import *

def splitter(x, fname="universalscrape.csv"):
	site = S_base(x).sel_soup()
	table = site.find('table',{'class':'productstable'}).tbody
	rows = table.find_all('tr')
	results = []
	d = {}
	publisher = ''
	for i in range(0, len(rows)):
		if check_element(rows[i],'class', 'liRow') or check_element(rows[i], 'class', 'liAlternate'):
			print("Worked")
			cells = rows[i].find_all('td')
			new_item = []
			inner_t = rows[i].find('table')
			product_name = con_text_s(inner_t.find('td'))
			image_link = 'http://www.universaldist.com/' + S_format(str(rows[i].find('a', {'class':'ProductIconImage'}))).linkf('href=')
			image_name = fn_grab(image_link)
			rows[i].find('table').parent.decompose() #removes the table and its td parent tag from row
			sku = con_text_s(rows[i].find('td'))
			new_item = (product_name, image_link, image_name, sku, publisher)
			results.append(new_item)
		if check_element(rows[i], 'class', 'category'):
			category_name = [con_text_s(rows[i])]
			publisher = category_name[0].split('/')[1].strip(' ')
			results.append(tuple(category_name))
	w_csv(results, fname)
	return results

def check_element(x, attr, attr_v=''):
	try:
		x[attr]
	except KeyError:
		#returns False if the element doesn't have the specific attribute
		return False
	except TypeError:
		#returns False if x isn't actually a bs element
		return False
	else:
		#returns True if the element has the specific attribute
		if x[attr] == [attr_v]:
			return True
		else:
			return False
if __name__ == '__main__':
	if sys.argv[1] == '-lw':
		splitter('https://www.universaldist.com/pre-orders.aspx?Command=LastWeek', sys.argv[2])
	else:
		splitter('http://www.universaldist.com/pre-orders.aspx', sys.argv[1])

#test = splitter('http://www.universaldist.com/pre-orders.aspx')
#test_1_site = S_base('http://www.universaldist.com/pre-orders.aspx').sel_soup()
#test_1_table = test_1_site.find('table',{'class':'productstable'}).tbody
#rows = test_1_table.find_all('tr')