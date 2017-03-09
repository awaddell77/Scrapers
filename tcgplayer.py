#tcgplayer scrape
from soupclass8 import *

browser = Sel_session('http://www.tcgplayer.com/')
browser.start()
magic_crit = ["Name", "Card Type:", "P / T:", "Rarity", "Card Number", "Description:", "Set Name:", "Color"]
fow_crit = ["Name", "Type:", "Atk / Def:", "Rarity", "Card Number", "Description:", "Set Name:", "Attribute:", "Cost:", "Race:"]
results = [["Name", "Card Type", "Pow/Tgh", "Rarity", "Card Number", "Card Text", "Set Name", "Finish", "Color", "Cost", "Artist"]]
results_fow = [["Name", "Card Type", "ATK/DEF", "Rarity", "Card Number", "Card Effect", "Set Name", "Attribute", "Cost", "Race"]]
def splitter_fow(x, color = 0):
	d = {}
	browser.go_to(x)
	browser.w_load(30)
	print("Processing {0}".format(x))
	site = browser.source()
	d["Name"] = site.find('div', {'class':'cardDetails'}).h1.text
	table = site.find('div', {'class':'cardDetails'}).table
	rows = table.find_all('tr')
	image_link = S_format(str(site.find('div', {'class':'detailImage'}))).linkf('src=', 0, '<img')
	d["Product Image"] = fn_grab(image_link)
	d["Image Link"] = image_link
	if color != 0:
		d["Color"] = color
	for i in range(0, len(rows)):
		if rows[i].find('td').text == 'Rarity / #:':
			contents = re.sub('\n', ' ', rows[i].find('td').find_next('td').text).split('/')
			d['Rarity'] = contents[0].strip(' ')
			d['Card Number'] = contents[1].strip(' ')
		else:
			d[re.sub('\n', '' , rows[i].find('td').text)] = re.sub('\n', '', rows[i].find('td').find_next('td').text).strip(' ')
	return S_format(d).d_sort(fow_crit)

def splitter_magic(x, color = 0):
	d = {}
	browser.go_to(x)
	browser.w_load(30)
	print("Processing {0}".format(x))
	site = browser.source()
	d["Name"] = site.find('div', {'class':'cardDetails'}).h1.text
	table = site.find('div', {'class':'cardDetails'}).table
	rows = table.find_all('tr')
	if color != 0:
		d["Color"] = color
	for i in range(0, len(rows)):
		if rows[i].find('td').text == 'Rarity, #:':
			contents = re.sub('\n', ' ', rows[i].find('td').find_next('td').text).split(',')
			d['Rarity'] = contents[0]
			d['Card Number'] = contents[1].strip(' ')
		else:
			d[re.sub('\n', '' , rows[i].find('td').text)] = re.sub('\n', '', rows[i].find('td').find_next('td').text)
	return S_format(d).d_sort(magic_crit)


def link_collector():
	#grabs all the links on a single results page on TCG Player
	#browser.go_to(x)
	time.sleep(2)
	test = browser.source() #test is used as the identifier because I don't want to find and replace for it in this function
	links = ['http://shop.tcgplayer.com' + S_format(str(test.find_all('div', {'class':'sellerContainer'})[i].a)).linkf('<a href=') for i in range(0, len(test.find_all('div', {'class':'sellerContainer'})))]
	return links



def main_magic_full(x, total = 0):
	browser.go_to(x)
	results = [["Name", "Card Type", "Pow/Tgh", "Rarity", "Card Number", "Card Text", "Set Name", "Color", "Finish", "Cost", "Artist"]]
	links = []
	while True:
		#gets links for the entire set
		time.sleep(2)
		links.extend(link_collector())
		if browser.driver.execute_script("return document.getElementsByClassName('nextPage')[0].getAttribute('disabled')") == "disabled":
			break
		else:
			browser.driver.execute_script("document.getElementsByClassName('nextPage')[0].click()")
	if total != 0 and len(links) < total:
		print("Found less than the total")
		return results


	for i in range(0, len(links)):
		results.append(splitter_magic(links[i], color))
	w_csv(results, 'tcgplayer.csv')
	return results
def main_fow_full(x, total = 0):
	browser.go_to(x)
	results_fow = [["Name", "Card Type", "ATK/DEF", "Rarity", "Card Number", "Card Effect", "Set Name", "Attribute", "Cost", "Race"]]
	links = []
	while True:
		#gets links for the entire set
		time.sleep(2)
		links.extend(link_collector())
		if browser.driver.execute_script("return document.getElementsByClassName('nextPage')[0].getAttribute('disabled')") == "disabled":
			break
		else:
			try: 
				browser.driver.execute_script("document.getElementsByClassName('nextPage')[0].click()")
			except:
				browser.driver.refresh()
	if total != 0 and len(links) < total:
		print("Found less than the total")
		return results


	for i in range(0, len(links)):
		results_fow.append(splitter_fow(links[i]))
	w_csv(results_fow, 'tcgplayer.csv')
	return results

#test = main_magic_full("http://shop.tcgplayer.com/magic/modern-masters-2017?ProductType=Singles")
test = main_fow_full("http://shop.tcgplayer.com/force-of-will/return-of-the-dragon-emperor")



def new_find(new, old):
	new_f = r_csv(new)
	old_f = r_csv(old)
	new_entries = [new_f[0]]
	check = ''

	for i in range(1, len(new_f)):
		check = True
		for i_2 in range(1, len(old_f)):
			if new_f[i][0] == old_f[i_2][0]:
				check = False
		if check:
			new_entries.append(new_f[i])
	w_csv("new_cards.csv")
	return new_entries




