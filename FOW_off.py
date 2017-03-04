
#fow official fow (http://fowtcg.com/cards/flame/VIN002/)
from soupclass8 import *
from Im_dwnld import *
import sys

def main(x, img_d = 0):
	print(x)
	if '.txt' in x:
		urls = link_grab(text_l(x))
	else:
		urls = link_grab(x)
	results = [["Card Name", "Card Number", "Rarity", "Card Type", "Race", "Product Image", "ATK/DEF", "Card Effect",'Image Link', 'Attribute','Edition', 'Set Name' ]]
	for i in range(0, len(urls)):
		results.append(splitter(urls[i]))

	if img_d != 0:
		img_link = [results[i][8] for i in range(0, len(results))]
		Im_dwnld('FOW').main_i(img_link)

	w_csv(results)
	return results
def all_main(x, img_d=0):
	url = 'http://fowtcg.com/cards/'
	types = ['light', 'flame', 'water', 'wind', 'darkness', 'ne']
	results = []
	for i in range(0, len(types)):
		full_url = url + types[i] + '/' + str(x) 
		results.extend(main(full_url, img_d))
	w_csv(de_dupe(results))
	return de_dupe(results)

def de_dupe(x):
	#removes duplicates from csv files
	#increments must be negative to avoid throwing loop off
	for i in range(len(x)-1,0, -1):
		#second loop starts where the first loop is currently located (i)
		for i_2 in range(len(x)-1, i, -1):
			if x[i][0] == x[i_2][0]:
				x.remove(x[i])
				print("Removing {0}".format(x[i][0]))
	return x

def splitter(x):
	site = S_base(x).soupmaker()
	d = {}
	card_table = site.find('div', {'id':'main_body'})
	card_name = site.find('td',{'class':'card_name'}).text
	card_info_r = card_table.find('tr', {'class':'card_info'}).find_all('td')
	card_info = [card_info_r[i].text for i in range(0, len(card_info_r))] #grabs the card number, rarity, type, etc
	card_attk = re.sub('ATK/','', card_table.find('td', {'class':'card_atk'}).text)
	card_def = re.sub('DEF/','', card_table.find('td', {'class':'card_def'}).text)
	card_AD = card_attk + ' / ' + card_def
	card_ability = 'None'
	card_image_link = 'None'
	card_image = 'fow-cardback.jpg'
	if card_table.find('div', {'class':'detail_img'}).img != None:
		card_image_link = 'http://fowtcg.com' + S_format(str(card_table.find('div', {'class':'detail_img'}).img)).linkf('src=')
		card_image = fn_grab(card_image_link)
	if card_table.find('dl', {'class':'card_ability'}).text != None:
		card_ability = re.sub('\n',' ', card_table.find('dl', {'class':'card_ability'}).text).strip(' ')
	card_info.insert(0, card_name)
	card_info.extend([card_image, card_AD, card_ability, card_image_link])
	return tuple(card_info)

def link_grab(x):
	results = []
	if '.txt' in x:
		#takes file name, returns links
		urls = text_l(x)
	else:
		urls = x
	if type(x) == str:
		site = S_base(urls).soupmaker()
		links = site.find('ul', {'id':'card_list'}).find_all('a')
		new = ['http://fowtcg.com' + S_format(str(links[i])).linkf('<a href=') for i in range(0, len(links))]
		results.extend(new)
		return results
	else:
		for i in range(0, len(urls)):
			site = S_base(urls[i]).soupmaker()
			links = site.find('ul', {'id':'card_list'}).find_all('a')
			new = ['http://fowtcg.com' + S_format(str(links[i])).linkf('<a href=') for i in range(0, len(links))]
			results.extend(new)
		return results

if len(sys.argv) > 1:
	if sys.argv[1] == '-m':
		all_main(sys.argv[2])
	else:
		main(sys.argv[1])
else:
	print("[link]")

