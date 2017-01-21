#for scraping from http://cf-vanguard.com/en/cardlist/
from soupclass8 import *
import sys



def main(x):
	site = Sel_session()
	#link results
	results_cd = [["Name", "Trigger", "Rarity", "Clan", "Card Number", "Shield", "Set Name", "Power", "Unit", "Grade / Skill","Race","", "Critical", "Card Effect"]]
	#card data results
	results = []
	site.go_to(x)
	#bsObject = site.source()
	wait = WebDriverWait(site.driver, 10)
	items = site.js('''return document.getElementsByClassName('pageLink')[0].children''')
	while site.js('''return document.getElementsByClassName('pageLink')[0].children[{0}].className'''.format(len(items)-1)) == "":
		bsObject = site.source()
		results.extend(link_grab(bsObject))
		site.js('''document.getElementsByClassName('pageLink')[0].children[{0}].click()'''.format(len(items)-1))
		wait.until(EC.element_to_be_clickable((By.ID,'expansionDetail')))
		wait.until(EC.element_to_be_clickable((By.ID,'expansionDetail_table')))
	results.extend(link_grab(site.source()))
	for i in range(0, len(results)):
		results_cd.append(splitter(results[i]))
	site.close()
	w_csv(results_cd, "CFVGResults.csv")

	return results_cd

def link_grab(x):
	base = 'http://cf-vanguard.com/en/cardlist'
	bsObject = x
	table = bsObject.find('div', {'id':'expansionDetail_table'})
	table_obj = S_table(table)
	link_elements  = table_obj.table_eater_exp('a',2, 4, 'td')
	links = [S_format(str(link_elements[i])).linkf('href=', base, 1) for i in range(0, len(link_elements))]
	return links



def splitter(x):#is fed table
	
	print(x)
	bsObject = S_base(x).soupmaker()
	table = bsObject.find('div', {'id': 'cardDetail'})
	headers = table.find_all('th')
	d={}
	for i in range(0, len(headers)):
		if headers[i].text != "Illustrator":
			cell = headers[i].find_next_sibling()
			d[re.sub('\n', '', headers[i].text)] = cleaner(cell.text, ['\n', '\r'])
	return S_format(d).d_sort()

#test_s = S_base("http://cf-vanguard.com/en/cardlist/?cardno=G-TD09/019EN").soupmaker()
#result = splitter(test_s)
#test_results = main("http://cf-vanguard.com/en/cardlist/?cardno=G-TD09/001EN")
if len(sys.argv) > 1:
	main(sys.argv[1])
