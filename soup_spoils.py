#scrapes data from http://spoilsinventory.com/index.php
from soupclass7 import *



def main_test(x):
	bsObject = soup_maker('http://spoilsinventory.com/index.php')
	return cardinfo(splitter(bsObject))

def soup_maker(x,cat='Shade of the Devoured Emperor'):
	browser = webdriver.Firefox()
	browser.get(x)
	element = browser.find_element_by_name('edition[]')
	element.send_keys(cat)
	element2 = browser.find_element_by_xpath("//input[@value='Search']") #the search button
	element2.click()
	bsObject = bs(browser.page_source, 'lxml')
	browser.quit()
	return bsObject

def splitter(x):
	cards = x.find_all('table', {'class':'cardresult'})
	new = [[cards[i].find('td',{'class':'cardname'}), cards[i].find('td',{'class':'cardinfo'})] for i in range(0, len(cards))]
	return new


def cardinfo(x):
	#splits the cardinfo data by </br> tag, then it re-parses it as html in order to grab the text
	results = []
	for i in range(0, len(x)):
		text = str(x[i][1])
		text1 = text.split('</br>')
		for i_2 in range(0, len(text1)): #loops through the list that has been split by the '</br>' tag
			text1[i_2] = bs(text1[i_2], 'lxml')
			text1[i_2] = text1[i_2].text
			text1[i_2] = text1[i_2].split('\n')
			text1[i_2] = [S_format(spacesmash(text1[i_2][i_3])).encoder() for i_3 in range(0, len(text1[i_2])) ]
			text1[i_2].insert(0, S_format(x[i][0].text).encoder('\n'))
			text1[i_2].insert(1, S_format(str(x[i][0].a)).linkf('<a href='))
			text1[i_2].insert(2, fn_grab(S_format(str(x[i][0].a)).linkf('<a href=')))

		text = text1
		results.extend(text)
	w_csv(results, 'TEST.csv')
	return results





