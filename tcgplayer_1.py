#tcgplayer scrape
from soupclass8 import *
from Im_dwnld import *



browser = Sel_session('http://www.tcgplayer.com/')
browser.start()
magic_crit = ["Name", "Card Type:", "P / T:", "Rarity", "Card Number", "Description:", "Set Name:", "Color", "Product Image"]
fow_crit = ["Name", "Type:", "Atk / Def:", "Rarity", "Card Number", "Description:", "Set Name:", "Attribute:", "Cost:", "Race:"]
ws_crit = ["Name", "Rarity", "Card Number", "Level:", "Cost:", "Soul:", "Card Type:", "Trait:", "Color:", "Power:", "Trigger:", "Description:", "Product Image"]

pkm_crit = ["Name", "Card Type", "Rarity", "Card Number", "Card Text", "Attack #1", "Attack #2", "Attack #3", "HP", "Stage", "Ability", "Weakness", "Resistance", "Retreat Cost" "Set Name:", "Product Image"]
results = [["Name", "Card Type", "Pow/Tgh", "Rarity", "Card Number", "Card Text", "Set Name", "Finish", "Color", "Cost", "Artist"]]
results_fow = [["Name", "Card Type", "ATK/DEF", "Rarity", "Card Number", "Card Effect", "Set Name", "Attribute", "Cost", "Race"]]
results_ws = [["Name", "Rarity", "Card Number", "Level", "Cost", "Soul", "Card Type", "Trait", "Color", "Power", "Trigger", "Description"]]
results_pkm = [pkm_crit]

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
			d[re.sub('\n', ' ' , rows[i].find('td').text)] = re.sub('\n', '', rows[i].find('td').find_next('td').text).strip(' ')
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
	image_link = S_format(str(site.find('div', {'class':'detailImage'}))).linkf('src=', 0, '<img')
	d["Product Image"] = fn_grab(image_link)
	if color != 0:
		d["Color"] = color
	for i in range(0, len(rows)):
		if rows[i].find('td').text == 'Rarity, #:':
			contents = re.sub('\n', ' ', rows[i].find('td').find_next('td').text).split(',')
			d['Rarity'] = contents[0]
			d['Card Number'] = contents[1].strip(' ')
		elif rows[i].find('td').text == 'Description:':
			d[re.sub('\n', '' , rows[i].find('td').text)] = re.sub('\n', ' ', rows[i].find('td').find_next('td').text)

		else:
			d[re.sub('\n', '' , rows[i].find('td').text)] = re.sub('\n', ' ', rows[i].find('td').find_next('td').text)
	dwnld_obj = Im_dwnld('Magic Set')
	dwnld_obj.i_main([image_link])

	return S_format(d).d_sort(magic_crit)

def splitter_ws(x, color = 0):
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
			card_num = '/'.join(contents[1:]).strip(' ')
			#TCG Player adds the rarity onto the end of the number
			d['Card Number'] = card_num.split(' ')[0]

		else:
			d[re.sub('\n', ' ' , rows[i].find('td').text)] = re.sub('\n', '', rows[i].find('td').find_next('td').text).strip(' ')
	dwnld_obj = Im_dwnld('WS Set')
	dwnld_obj.i_main([image_link])

	return S_format(d).d_sort(ws_crit)
def splitter_pkm(x):
	d = {"Attack #1": '', "Attack #2":'', "Attack #3":'', "Ability":'', "Card Text":'', "Weakness":'', "Resistance":'', "Retreat Cost":'', "HP":''}
	browser.go_to(x)
	browser.w_load(30)
	print("Processing {0}".format(x))
	site = browser.source()
	d["Name"] = site.find('div', {'class':'cardDetails'}).h1.text
	table = site.find('div', {'class':'cardDetails'}).table
	rows = table.find_all('tr')
	image_link = S_format(str(site.find('div', {'class':'detailImage'}))).linkf('src=', 0, '<img')
	d["Product Image"] = fn_grab(image_link)
	for i in range(0, len(rows)):
		if rows[i].find('td').text == 'Card Number / Rarity:':
			contents = re.sub('\n', ' ', rows[i].find('td').find_next('td').text).split('/')
			d['Card Number'] = contents[0].strip(' ')
			d['Rarity'] = contents[1].strip(' ')
		elif rows[i].find('td').text == 'Card Type / HP / Stage:':
			contents = re.sub('\n', ' ', rows[i].find('td').find_next('td').text).split('/')
			d["Card Type"] = contents[0].strip(' ')
			d["HP"] = contents[1].strip(' ')
			d["Stage"] = contents[2].strip(' ')




		elif rows[i].find('td').text == 'Card Text:':
			value = re.sub('\n', ' ', rows[i].find('td').find_next('td').text)
			if "Ability —" in value:
				d["Ability"] = value
			else:
				d["Card Text"] = value
			#d[re.sub('\n', '' , rows[i].find('td').text)] = re.sub('\n', ' ', rows[i].find('td').find_next('td').text)
		elif 'Attack' in rows[i].find('td').text:
			if '1' in rows[i].find('td').text:
				d["Attack #1"] = rows[i].find('td').find_next('td').text.replace('\n', ' ').strip(' ')
			elif '2' in rows[i].find('td').text:
				d["Attack #2"] = rows[i].find('td').find_next('td').text.replace('\n', ' ').strip(' ')
			elif '3' in rows[i].find('td').text:
				d["Attack #3"] = rows[i].find('td').find_next('td').text.replace('\n', ' ').strip(' ')
		elif rows[i].find('td').text == 'Weakness / Resistance / Retreat Cost:':
			contents = re.sub('\n', ' ', rows[i].find('td').find_next('td').text).split('/')
			d["Weakness"] = contents[0].strip(' ')
			d["Resistance"] = contents[1].strip(' ')
			d["Retreat Cost"] = contents[2].strip(' ')




		else:
			d[re.sub('\n', '' , rows[i].find('td').text)] = re.sub('\n', ' ', rows[i].find('td').find_next('td').text)
	dwnld_obj = Im_dwnld('PKM Set')
	dwnld_obj.i_main([image_link])
	#return d
	return S_format(d).d_sort(pkm_crit)

def link_collector():
	#grabs all the links on a single results page on TCG Player
	#browser.go_to(x)
	time.sleep(2)
	test = browser.source() #test is used as the identifier because I don't want to find and replace for it in this function
	links = ['http://shop.tcgplayer.com' + S_format(str(test.find_all('div', {'class':'sellerContainer'})[i].a)).linkf('<a href=') for i in range(0, len(test.find_all('div', {'class':'sellerContainer'})))]
	return links



def main_magic_full(x,color= 0, total = 0):
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
	browser.close()
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
def main_ws_full(x, total = 0):
	browser.go_to(x)
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
		results_ws.append(splitter_ws(links[i]))
	w_csv(results_ws, 'tcgplayer_ws.csv')
	browser.close()
	return results
def main_pkm_full(x):
	browser.go_to(x)
	results = results_pkm
	links = []
	while True:
		#gets links for the entire set
		time.sleep(2)
		links.extend(link_collector())
		if browser.driver.execute_script("return document.getElementsByClassName('nextPage')[0].getAttribute('disabled')") == "disabled":
			break
		else:
			browser.driver.execute_script("document.getElementsByClassName('nextPage')[0].click()")


	for i in range(0, len(links)):
		results.append(splitter_pkm(links[i]))
	w_csv(results, 'tcgplayer.csv')
	browser.close()
	return results

#test = main_magic_full("http://shop.tcgplayer.com/magic/modern-masters-2017?ProductType=Singles")
#test = main_fow_full("http://shop.tcgplayer.com/force-of-will/return-of-the-dragon-emperor")



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




if __name__ == "__main__":
	if sys.argv[1] == "-magic":
		main_magic_full(sys.argv[2])
	elif sys.argv[1] == '-fow':
		main_fow_full(sys.argv[2])
	elif sys.argv[1] == '-ws':
		main_ws_full(sys.argv[2])
	elif sys.argv[1] == '-pkm':
		main_pkm_full(sys.argv[2])