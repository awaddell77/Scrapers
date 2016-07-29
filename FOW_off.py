
#fow official fow (http://fowtcg.com/cards/flame/VIN002/)
from soupclass8 import *

def main(x):
	urls = text_l(x)
	results = []
	for i in range(0, len(urls)):
		results.append(splitter(urls[i]))
	w_csv(results)
	return results

def splitter(x):
	site = S_base(x).soupmaker()
	card_table = site.find('div', {'id':'main_body'})
	card_name = site.find('td',{'class':'card_name'}).text
	card_info_r = card_table.find('tr', {'class':'card_info'}).find_all('td')
	card_info = [card_info_r[i].text for i in range(0, len(card_info_r))] #grabs the card number, rarity, type, etc
	card_attk = card_table.find('td', {'class':'card_atk'}).text
	card_def = card_table.find('td', {'class':'card_def'}).text
	card_ability = 'None'
	card_image_link = 'None'
	card_image = 'fow-cardback.jpg'
	if card_table.find('div', {'class':'detail_img'}).img != None:
		card_image_link = S_format(str(card_table.find('div', {'class':'detail_img'}).img)).linkf('src=')
		card_image = fn_grab(card_image_link)
	if card_table.find('dl', {'class':'card_ability'}).text != None:
		card_ability = re.sub('\n',' ', card_table.find('dl', {'class':'card_ability'}).text).strip(' ')
	card_info.insert(0, card_name)
	card_info.extend([card_image, card_attk, card_def, card_ability, card_image_link])
	return tuple(card_info)

def link_grab(x):
	#takes file name, returns links
	urls = text_l(x)
	results = []
	for i in range(0, len(urls)):
		site = S_base(urls[i]).soupmaker()
		links = site.find('ul', {'id':'card_list'}).find_all('a')
		new = ['http://fowtcg.com' + S_format(str(links[i])).linkf('<a href=') for i in range(0, len(links))]
		results.extend(new)
	return results

