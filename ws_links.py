

#for grabbing links from http://ws-tcg.com/en/cardlist/list/
from soupclass8 import *
import sys

browser = webdriver.Firefox()

def link_grab(set_name):
	links = []
	browser.get('http://ws-tcg.com/en/cardlist/list/')
	try:
		browser.find_element_by_link_text(set_name)
	except:
		print("Could not find set")
		return
	else:
		browser.find_element_by_link_text(set_name).click()

	buttons = len(browser.find_elements_by_xpath("//p[@class='pageLink']/*"))  #grabs link bar elements
	for i in range(0, buttons-4):
		#only needs to click a specific number of times
		
		site = bs(browser.page_source, 'lxml')
		links.extend(table_links(site))
		browser.find_elements_by_xpath("//p[@class='pageLink']/*")[buttons-1].click()
	return links


def table_links(x):
	site = x #must be beautifulsoup object
	table = site.find('div', {'id':'expansionDetail_table'})
	links_r = S_table(table).table_eater_exp('a',2,5)
	new = ["http://ws-tcg.com/en/cardlist/list" + re.sub('./','/', S_format(str(links_r[i])).linkf('<a href=')) for i in range(0, len(links_r))]
	return new
if len(sys.argv) != 1:
	link_grab(sys.argv[1])
else:
	print("[set name]")