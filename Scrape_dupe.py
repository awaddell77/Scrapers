#checks for duplicates in catalog
from Cat_dbase import *
from dictionarify import *
class Scrape_dupe:
	def __init__(self):
		self.cat_inst = Cat_dbase()
		self.cat_inst.set_proper_desc(True)
		#if scope_full is True then the entire catalog will be searched
		#if Flase only the target category is searched
		self.__scope_full = False
		self.__target_cat = ''
		self.__items = []
		self.__cat_items = []
		self.comp_res = []
		self.test_lst = []

	def search_scope(self):
		return self.__scope_full
	def set_search_scope(self, x):
		if not isinstance(x, bool):
			raise TypeError("Param must be bool")
		else:
			self.__generic = x
	def get_target_cat(self):
		return self.__target_cat
	def set_target_cat(self, x):
		self.__target_cat = x

	def get_items(self):
		return self.__items
	def set_items(self, x):
		self.__items = x
	def get_cat_items(self):
		return self.__cat_items
	def set_cat_items(self, x):
		self.__cat_items = x
	def import_items(self, x):
		if isinstance(x, list):
			self.set_items(x)
		else:
			self.set_items(dictionarify(x))
	def check_for_dupes(self, crit):
		results = []
		products_raw = self.cat_inst.get_category_contents(self.__target_cat)
		products = [i[crit] for i in products_raw]
		self.test_lst = products


		for i in self.__items:
			if i[crit] not in products:
				results.append(i)
		self.comp_res = results 
		return results




