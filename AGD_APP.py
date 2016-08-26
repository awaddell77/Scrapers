from soupclass8 import *


#AGD scraper (example: https://retailerservices.alliance-games.com/Login/Login?ReturnUrl=%2f)

#from AGD1 import *

browser = webdriver.Firefox()
browser.get('https://retailerservices.alliance-games.com/Login/Login?ReturnUrl=%2f')
username = input("Username: ")
password = input("Password: ")
element = browser.find_element_by_id('UserName')
element1 = browser.find_element_by_id('Password')
submission = browser.find_element_by_id('Submit')
element.send_keys(username)
element1.send_keys(password)
submission.click()


def item_search_category(category,wait=5):
	browser.find_element_by_link_text('Item Search').click()
	
	status = browser.find_element_by_id('OptionStatusIdx')
	status.send_keys('Not Yet Available')
	order_type = browser.find_element_by_id('OptionItemOrderTypeIdx')
	order_type.send_keys('Preorderable Items Only')
	search_button = browser.find_element_by_id('btnSearchItems')
	#browser.find_element_by_name('Category').click()
	cats = browser.find_elements_by_name('Category')
	#cat = browser.find_element_by_name('Category')

	links = []
	'''for i in range(0, len(cats)):
		cats[i].click()
		search_button.click() #searches'''
	return test(cats[1],wait)
def test(x,wait=5):
	x.click()
	search_button = browser.find_element_by_id('btnSearchItems').click()
	#if browser.find_element_by_class_name('PageSubTitle SearchResultsTitle') 
	browser.implicitly_wait(wait)
	results = result_grab(1)
	return results

def result_grab(x):
	links = []

	while browser.find_element_by_class_name('dgv-pager-next').is_enabled():
		source = browser.page_source
		links.extend(link_scrape(source))
		browser.find_element_by_class_name('dgv-pager-next').click() #continously clicks "NEXT" button 

	if browser.find_element_by_class_name('dgv-pager-next').is_enabled() == False:
			source = browser.page_source
			links.extend(link_scrape(source))
	if links == []:
		return "No Items Found"
	elif links == [[]]:
		return "Either no links were found on the table or no table was returned"
	#text_wc(listify(links), 'AGD.txt')
	new = [item_scrape(links[i]) for i in range(0, len(links))]
	return new
def browser_grab(x):
	#starts from the current page the driver is on
	new = result_grab(1)
	w_csv(new)
	return new


def browser_source(x):
	return browser.page_source

def link_scrape(source):
	bsObject = bs(source, 'lxml')
	if bsObject.find('table') != None:
		t_links = bsObject.find('table').find_all('a', {'class':'fancybox'})
		links = ['https://retailerservices.alliance-games.com' + S_format(str(t_links[i])).linkf('href=') for i in range(0, len(t_links))]
		return dupe_erase(links)
	else:
		return []

def item_scrape(x):
	browser.get(x)
	d = {}
	source = browser.page_source
	bsObject = bs(source, 'lxml')
	title = re.sub('\n', '', bsObject.find('div',{'class':'Description'}).text)
	d['Title'] = title
	table = bsObject.find('table', {'class':'ItemDetailTable'})
	if table == None:
		return 'Could not find table for %s' % (x)

	headers = table.find_all('th')
	for i in range(0, len(headers)):
		if headers[i].find_next_sibling('td') != None:
			try:
				d[re.sub('\n', '', headers[i].text)] = re.sub('\n', '', headers[i].find_next_sibling('td').text)
			except AttributeError as AE:
				d[re.sub('\n', '', headers[i].text)] = "None"
	return S_format(d).d_sort(1)

