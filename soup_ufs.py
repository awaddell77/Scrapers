#UFS scraper
from soupclass8 import *
from bs4 import BeautifulSoup as bs
import time
class UfsScraper:
	def __init__(self, set_name):
		self.set_name = set_name
		self.site = None
	def main(self):
		site = Sel_session()
		site.go_to("http://ufsultra.com/")
		command = """ 
			var options = document.getElementById('extension')
			for (i = 0; i < options.length; i++){{
				if(options.children[i].innerHTML == \"{0}\"){{
					options.children[i].selected = true;
				}}
				
				}}

			var s_button = document.getElementById('search_buttons').children[1];
			s_button.click();



			""".format(str(self.set_name))
		print(command)
		try:
			site.driver.execute_script(command)
		except:
			print("Error occured while trying to select proper category/set")
			site.close()
		limit = int(site.driver.execute_script("return document.getElementsByClassName('pagination pagination-sm')[1].children")) - 1
		while(True):
			time.sleep(3)
			self.cardInfoScrape(site.source())
			button_check = site.driver.execute_script("return document.getElementsByClassName('pagination pagination-sm')[1].children[{0}].getAttribute('class') == \"disabled\"".format(limit))
			if (button_check):
				break
			else:
				site.driver.execute_script("return document.getElementsByClassName('pagination pagination-sm')[1].children[{0}].click()".format(str(limit)))

		site.close()
	def cardInfoScrape(self, x):
		pass





test = UfsScraper("Street Fighter")
test.main()




