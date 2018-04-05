#magic 
#srapes a set page http://gatherer.wizards.com/Pages/Search/Default.aspx?set=[%22Duel%20Decks:%20Mind%20vs.%20Might%22]
from soupclass8 import *

import time
class Magic_scrape:
	def __init__(self, url):
		self.url = url
		self.session = Sel_session(url)
		self.cards = []
		self.headers = ["Name", "Card Type", "Pow / Tgh", "Card Text", "Rarity", "Color", "Cost", "Image Link"]
	def browser_start(self):
		self.session.start()


	def page_scrape(self):
		card_table_rows = []
		while(True):
			site = self.session.source()
			card_table = site.find('table',{'class':'cardItemTable'})
			card_table_rows.extend(card_table.find_all('tr', {'class':'cardItem evenItem'}))
			card_table_rows.extend(card_table.find_all('tr', {'class':'cardItem oddItem'}))
			command = '''
			function pageCheck(){
			var res = true
			var h =  "ctl00_ctl00_ctl00_MainContent_SubContent_topPagingControlsContainer";
			var element = document.getElementById(h).children[document.getElementById(h).children.length - 1];
			if (element.getAttribute("style") == "visibility:hidden;" && !(element.getAttribute("style") === null) ){
				return false;
			}
			return true}
			return pageCheck()
			'''
			test =  self.session.driver.execute_script(command)
			print(test)
			if test:
				print("RETURNED TRUE")
				command1 = '''

				var buttons = document.getElementById("ctl00_ctl00_ctl00_MainContent_SubContent_topPagingControlsContainer");
				var element = buttons.children[buttons.children.length - 1]
				element.click();'''
				self.session.driver.execute_script(command1)
				time.sleep(3)

			elif not self.session.driver.execute_script("return {0}".format(command)):
				break

		#card_info = [i.find('div', {'class':'cardInfo'}) for i in card_table_rows]
		for i in card_table_rows:
			self.cards.append(self.__card_info_get(i))
		#print(self.cards)
	def page_source(self):
		pass

	def __card_info_get(self, x):
		#takes the div class='cardInfo' element, returns dictionary with all the card values
		d = {}
		card_info = x.find('div', {'class':'cardInfo'})
		d["Name"] = re.sub('\n', '', card_info.find('span', {'class':'cardTitle'}).text)
		#print("Processing {0}".format(d["Name"]))
		type_attack = card_info.find('span', {'class':'typeLine'}).text
		mana = card_info.find("span",{'class':'manaCost'})
		cost_color = self.mana_cost(mana)
		d["Cost"] = cost_color[0]
		d["Color"] = cost_color[1]
		#artifact 

		if re.search('\(\d/\d\)', type_attack) != None:
			t_a = re.search('\(\d/\d\)', type_attack)
			d["Pow / Tgh"] = re.sub('\n', '', t_a.group())
			d["Card Type"] = re.sub('\n', '', type_attack.replace(d["Pow / Tgh"], '')).strip(' ')
		else:
			d["Card Type"] = re.sub('\n', '', type_attack).strip(' ')
			d["Pow / Tgh"] = ''
		d["Card Text"] = self.paragraph_form(card_info.find('div', {'class':'rulesText'})).text.replace('\n', ' ')
		rarity = S_format(str(x.find('td', {'class':'rightCol setVersions'}).find('div',{'class':'rightCol'}).img)).linkf('<img alt=')
		d["Rarity"] = self.rarity_find(rarity)
		if "Artifact" in d["Card Type"]:
			d["Color"] = "Artifact"
		elif "Land" in d["Card Type"]:
			d["Color"] = "Land"
		image_r = x.find('img')
		d["Image Link"] = ''
		if image_r is not None:
			d["Image Link"] = "http://gatherer.wizards.com/" + S_format(str(image_r)).linkf('src=').replace('../', '')
		return d
	def card_info(self,x):
		d = {}
		d["Color"] = ''
		site = S_base(x).soupmaker()
		cinfo = site.find('div', {'style':'margin-top: 5px;'})
		rows = cinfo.find_all('div',{'class':'label'})
		for i in range(0, len(rows)):
			print(rows[i])
			print('===================================================')
			print(rows[i].find_next())
			if 'Mana Cost' in rows[i].text and 'Converted' not in rows[i].text:
				d[cleaner(rows[i].text, ['\n', '\r', '\t',':']).strip()] = self.mana_cost(rows[i].find_next())[0]
				d["Color"] = self.mana_cost(rows[i].find_next())[1]
			else:
				d[cleaner(rows[i].text, ['\n', '\r', '\t',':']).strip()] = cleaner(rows[i].find_next().text, ['\n', '\r', '\t']).strip()
		return d



	def mana_cost(self, x):
		colors = {'Green':'G', 'Red':'R', "Black":"B", "Blue":"U", "White":"W", "Colorless":"C", "Variable Colorless":"X"}
		color = ''
		images = x.find_all('img')
		cost = ''
		for i in images:
			element = S_format(str(i)).linkf('alt=')
			if element.isdigit():
				cost += element
			elif not element.isdigit() and ' or ' in element:
				sects = element.split(' or ')
				cost += "(" + colors[sects[0]] + "/" + colors[sects[1]] + ")"

			else:
				cost += colors[element]
		for i in cost:
			#if i isn't a number and color has not been set
			if i == 'C' or i == 'X':
				color = ''
			if not i.isdigit() and not color:
				color = i
			elif '/' in cost:
				#need to add something here to check for hybrid mono-lands (See: "Beseech the Queen")
				color = "Multi-Color"
				return (cost, color)
			elif not i.isdigit() and '' not in color:
				color = "Mult-Color"
				return (cost, color)
			elif not i.isdigit() and color and color != i:
				color = "Multi-Color"
				return (cost, color)
			'''else:
				#remember to fix string after testing
				color = "ElseMulti-Color"
				return (cost, color)'''
		#possibly redundant return statement
		return (cost, self.color_trans(color))
	def color_trans(self, x):
		color_d = {'G':'Green', 'R':'Red', "B":"Black", "U":"Blue", "W":"White", "Colorless":"C", "Variable Colorless":"X", "Multi-Color":"Multi-Color",'':''}
		return color_d[x]


	def paragraph_form(self, x):
		x = self.p_image_process(x)
		if x.find('p') is not None:
			for i in x.find_all('p'):
				i.insert_after(' ')

		return x
	def p_image_process(self, x):
		colors = {'Green':'G', 'Red':'R', "Black":"B", "Blue":"U", "White":"W", "Colorless":"C", "Variable Colorless":"X", "Tap":"T"}
		images = x.find_all("img")
		if images is None:
			return x
		for i in images:
			#print(i)
			image = S_format(str(i)).linkf("alt=")
			#if i isn't a number and color has not been set
			if image.isdigit():
				i.replace_with(str(image))
			if not image.isdigit():
				i.replace_with(str(colors[image]))
		return x
	def m_csv(self):
		results = []
		results.append(self.headers)
		for i in self.cards:
			card = []
			for i_2 in self.headers:
				card.append(i[i_2])
			results.append(card)
		w_csv(results, "magic_set.csv")
	def pict_trans(self,x):
		if x.find('img') == None:
			return x
		else:
			x.find('img')
	def rarity_find(self, x):
		rarities = ['Rare', 'Common', 'Uncommon', 'Mythic Rare']
		for i in rarities:
			res = re.search('\({0}\)'.format(i), x)
			if res != None:
				return i[0]
		return 'Rarity Not Found'
	def sort_cards(self):
		#sorts the cards in the state
		self.cards = self.sort_output()

	def sort_output(self):
		#for now it will sort cards alphabetically by name
		return sorted(self.cards, key= lambda a: a['Name']) 



if __name__ == '__main__':
	mag_inst = Magic_scrape(sys.argv[1])
	mag_inst.browser_start()
	mag_inst.page_scrape()
	mag_inst.m_csv()
	mag_inst.session.close()





