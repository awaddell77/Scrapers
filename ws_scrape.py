from soupclass8 import *
from Im_dwnld import *
import sys


class Ws_scrape:
	def __init__(self):
		self.__set_name = ''
		self.__urls = ''
		self.__start = ''
		self.__scrape_results = ''
		self.__img_d = True
		self.__dir_name = 'WS Images'
	def get_set_name(self):
		return self.__set_name
	def set_set_name(self, x):
		self.__set_name = x
	def get_urls(self):
		return self.__urls
	def set_urls(self, x):
		self.__urls = x
	def get_start(self):
		return self.__start
	def set_start(self, x):
		self.__start = x
	def get_scrape_res(self):
		return self.__scrape_results
	def set_scrape_res(self, x):
		self.__scrape_results = x
	def get_img_dwnld(self):
		return self.__img_d
	def set_img_dwnld(self, x):
		if isinstance(x, bool):
			self.__img_d = x
		else:
			raise TypeError("Argument must be bool")




	def link_grab(self):
		browser = Sel_session()
		links = []
		browser.go_to('http://ws-tcg.com/en/cardlist/list/')
		set_name = self.get_set_name()
		url = self.get_start()
		#if url is '' it uses the set name
		if not url:
			try:
				browser.driver.find_element_by_link_text(set_name)
			except:
				print("Could not find set")
				
			else:
				browser.driver.find_element_by_link_text(set_name).click()
		else:
			browser.go_to(url)


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
			links.extend(self.table_links(site))
			browser.js('return document.getElementsByClassName("pageLink")[0].children[%s].click();' % (str(button_length-1)))
		#links.extend(table_links(browser.source()))
		#text_wc(links)
		self.set_urls(links)
		browser.close()
		return links


	def table_links(self, x):
		site = x #must be beautifulsoup object
		table = site.find('div', {'id':'expansionDetail_table'})
		links_r = S_table(table).table_eater_exp('a',2,5)
		new = ["http://ws-tcg.com/en/cardlist/list" + re.sub('\./','/', S_format(str(links_r[i])).linkf('href=',0, 1)) for i in range(0, len(links_r))]
		try:
			new.remove('http://ws-tcg.com/en/cardlist/listNone')
		except ValueError:
			return new
		else:
			return new


	def scrape_set(self):
	    urls = self.get_urls()
	    results = [['Card Name','Power', 'Type', 'Color', 'Card Text', 'Level', 'Soul', 'Rarity', 'Trigger', 'Traits', 'Cost', 'Card Number', 'Side', 'Expansion']]
	    for i in range(0, len(urls)):
	        #iterates through all of the fresh links
	        
	        if "listNone" not in urls[i]:
	        	print("Now Processing %s" % urls[i])
	        	bsObject = self.test(S_base(urls[i]).soupmaker())
	        	results.append(self.stsc(bsObject))
	    self.set_scrape_res(results)
	    w_csv(results)
	    print("Complete")
	    return results

	def test(self, x):#is fed table
	    bsObject = x
	    table = bsObject.find('div', {'id': 'cardDetail'})
	    headers = table.find_all('th')
	    d={}
	    for i in range(0, len(headers)):
	        cell = headers[i].find_next_sibling()
	        head = re.sub('\n', '', headers[i].text)
	        d[head] = cell
	    image_link = S_format(str(bsObject.find('td', {'class':'graphic'}).img)).linkf('src=')
	    d['Picture Link'] =  re.sub('\.\.', 'http://ws-tcg.com/en/cardlist', image_link)
	    d['Picture'] = fn_grab(d['Picture Link'])
	    if self.get_img_dwnld():
	    	dwnld_obj = Im_dwnld(self.__dir_name)
	    	dwnld_obj.i_main([d["Picture Link"]])

	    return d
	def uni_clean(self, x):
		chars = [('“', '\"'), ("”", '"'), ("’", "' "), ('【', '[') , ('】', ']'), ('《', '<<') ,('》', '>>'),
		('・', ' '), ('♪', '')
		]
		for i in chars:
			x = str(x).replace(i[0], i[1])
		return x
	    
	    
	'''FORMATTING'''
	def stsc(self, x):#takes dictionary
	    d = x
	    d['Card Name'] = d['Card Name'].span#prevents text method from doubling the name
	    need_1 = ['Card Name','Power', 'Card Type', 'Color', 'Text', 'Level', 'Soul', 'Rarity', 'Trigger', 'Special Attribute', 'Cost', 'Card No.', 'Side', 'Expansion', 'Picture', 'Picture Link']
	    pict = ['Color','Trigger','Soul', 'Side']
	    need_2 = ['Card Name','Power', 'Card Type', 'Text', 'Level', 'Rarity', 'Special Attribute', 'Cost', 'Card No.', 'Expansion']#need list sans the pictures
	    for i in range(0, len(pict)):
	        if pict[i] == 'Color' or pict[i] == 'Side':
	            new = S_format(str(d[pict[i]].img)).linkf('<img src=').split('/')
	            d[pict[i]] = new[len(new)-1]
	        else:
	            d[pict[i]] = len(d[pict[i]].find_all('img'))
	    for i in range(0, len(need_2)):
	        d[need_2[i]] = cleaner(d[need_2[i]].text, ['\n', '\t', '\r'])
	    d['Text'] = self.uni_clean(d['Text'])
	    d["Card Name"] = self.uni_clean(d['Card Name'])
	    d["Color"] = str(d["Color"].split('.')[0]).title()
	    d['Side'] = str(d['Side'].split('.')[0]).title()
	    d['Special Attribute'] = self.uni_clean(d['Special Attribute'])
	    return S_format(d).d_sort(need_1)

if __name__ == '__main__':
	ws_inst = Ws_scrape()
	#for set name
	if sys.argv[1] == '-sn':
		ws_inst.set_set_name(sys.argv[2])
	else:
		ws_inst.set_start(sys.argv[1])
	ws_inst.link_grab()
	ws_inst.scrape_set()
