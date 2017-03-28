#troll and toad
from soupclass8 import *
from Im_dwnld import *

class Tnt:
	def __init__(self, url):
		self.url = url
		self.__page_res = []
		self.__dlinks = []
		self.__d_opt = False
		self.__folder_name = ''
	def get_page_res(self):
		return self.__page_res
	def set_page_res(self, x):
		self.__page_res = x
	def get_dlinks(self):
		return self.__dlinks
	def set_dlinks(self, x):
		self.__dlinks = x
	def get_d_opt(self):
		return self.__d_opt
	def set_d_opt(self, x):
		if type(x) == bool:
			self.__d_opt = x
		else:
			raise TypeError("Argument must be bool (either \"True\" or \"False\"")
	def get_folder(self):
		return self.__folder_name
	def set_folder(self, x):
		self.__folder_name = x

	def page_scrape(self):
		bsObject = S_base(self.url).soupmaker()
		table = bsObject.find('div', {'class':'catResults'})
		rows = table.find_all('div', {'class':'cat_result_wrapper'})
		for i in range(0, len(rows)):
			image_link = S_format(str(rows[i].find('div',{'class':'cat_result_image_wrapper'}).img)).linkf('src=')
			image_link = image_link.replace('thumbnails','pictures')
			image_name = fn_grab(image_link)
			item_name = rows[i].find('div',{'class':'cat_result_text'}).h2.text
			item_name = item_name.strip(' ')
			self.__page_res.append([item_name, image_name, image_link])
			self.__dlinks.append(image_link)
		return self.get_page_res()
	def m_csv(self):
		headers = [["Product Name", "Product Image", "Image Link"]]
		new_lst = headers + self.get_page_res() 
		w_csv(new_lst, "tntfile.csv")
		if self.__d_opt:
			d_obj = Im_dwnld(self.get_folder())
			d_obj.i_main(self.get_dlinks())

'''test_inst = Tnt('http://www.trollandtoad.com/YuGiOh/10329.html?orderBy=Alphabetical+A-Z&filterKeywords=&sois=Yes&minPrice=&maxPrice=&yuCardTypeSelect=Select+Card+Type&minLevelRank=&maxLevelRank=&minAttack=&maxAttack=&minDefense=&maxDefense=&pageLimiter=100&showImage=Yes&PageNum=')
test_inst.page_scrape()
test_inst.set_d_opt(True)
test_inst.set_folder("Unlimited Singles")
test_inst.m_csv()'''





