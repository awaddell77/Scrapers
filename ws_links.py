

#for grabbing links from http://ws-tcg.com/en/cardlist/list/
from soupclass8 import *
import sys

browser = Sel_session()

def link_grab(set_name):
	links = []
	browser.go_to('http://ws-tcg.com/en/cardlist/list/')
	try:
		browser.driver.find_element_by_link_text(set_name)
	except:
		print("Could not find set")
		return
	else:
		browser.driver.find_element_by_link_text(set_name).click()


	wait = WebDriverWait(browser.driver, 10)
	wait.until(EC.element_to_be_clickable((By.ID,'expansionDetail')))
	wait.until(EC.element_to_be_clickable((By.ID,'expansionDetail_table')))
	buttons = browser.js('return document.getElementsByClassName("pageLink")[0].children;')
	button_length = int(browser.js('return document.getElementsByClassName("pageLink")[0].children.length;'))
	#grabs link bar elements
	while browser.js('return document.getElementsByClassName("pageLink")[0].children[%s].className;' % (str(button_length-1))) == "":

		#only needs to click a specific number of times
		wait.until(EC.element_to_be_clickable((By.ID,'expansionDetail')))
		wait.until(EC.element_to_be_clickable((By.ID,'expansionDetail_table')))
		site = browser.source()
		links.extend(table_links(site))
		browser.js('return document.getElementsByClassName("pageLink")[0].children[%s].click();' % (str(button_length-1)))
	#links.extend(table_links(browser.source()))
	text_wc(links)
	return links


def table_links(x):
	site = x #must be beautifulsoup object
	table = site.find('div', {'id':'expansionDetail_table'})
	links_r = S_table(table).table_eater_exp('a',2,5)
	new = ["http://ws-tcg.com/en/cardlist/list" + re.sub('\./','/', S_format(str(links_r[i])).linkf('<a href=')) for i in range(0, len(links_r))]
	new.remove('http://ws-tcg.com/en/cardlist/listNone')
	return new
if len(sys.argv) != 1:
	link_grab(sys.argv[1])
else:
	print("[set name]")