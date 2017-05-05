#comic formatting
import sys
from r_csv_sa import *
from Im_dwnld import *
import re
from soupclass8 import w_csv, S_format
from Cat_dbase import *

class Comic:
	def __init__(self, fname = '', fname2 = ''):
		self.master = fname
		self.preview = fname2
		self.cat_obj = Cat_dbase()
		self.r_data = ''
		self.preview_data = ''
		self.comic_data = []
		self.genre_dict =  {'XX': '*No Genre* or *All Genre*', 'WR': 'War', 'YA': 'Yaoi', 'MS': 'Mystery', 
		'HS': 'Historical', 'SN': 'Seasonal', 'RL': 'Religious', 'AS': 'Art Supplies', 'AD': 'Adult', 'TY': 'Toy Tie-In', 
		'DR': 'Drama', 'GA': 'Gaming/Role Playing', 'PK': 'Pokémon', 'AN': 'Anthology', 'SP': 'Sports', 
		'RO': 'Romance', 'LT': 'Literary', 'CR': 'Crime', 'HT': 'How to Draw', 'HO': 'Horror', 'KI': 'Kids', 
		'LG': 'Legend', 'RB': 'Reality-Based', 'WS': 'Western', 'FA': 'Fantasy', 'SF': 'Science Fiction', 'MV': 'Movie/TV Tie-In',
		'SU': 'Surreal/Non-Linear', 'HA': 'Halloween', 'CJ': 'Comics Journalism','MU': 'Music', 'SH': 'Super-hero', 
		'AA': 'Action/Adventure', 'RF': 'Reference/Art Books/How To', 'MA': 'Manga', 'HU': 'Humor/Comedy', 
		'DT': 'Designer Toys', 'PC': 'Pop Culture', 'AP': 'Anthropomorphics'}
		self.cat_dict = {'15': 'Posters/Prints/Portfolios/Calendars', '4': 'Books - Science-Fiction/Horror/Novels', 
		'11': 'Supplies - Card', '10': 'Toys and Models', '13': 'Retailers Sales Tools', '16': 'Video/Audio/Video Games', 
		'6': 'Cards - Sports/Non-Sports', '1': 'Comics - Black & White/Color', '7': 'Novelties - Comic Material', 
		'3': 'Books - Illustrated Comic Graphic Novels/Trade Paperbacks', '14': 'Diamond Publications', '12': 'Supplies - Comic', 
		'9': 'Apparel - T-shirts/Caps', '8': 'Novelties - Non-Comic Material', '5': 'Games', '2': 'Magazines - Comics/Games/Sports'}
	def import_r_data(self):
		csv_inst = R_csv(self.master)
		csv_inst.delimiter = '\t'
		self.r_data = csv_inst.dictionarify()
		csv_inst.fname = self.preview
		csv_inst.set_headers(["DIAMD_NO", "FULL_TITLE", "SRP", "Description", "Credits"])
		self.preview_data = csv_inst.dictionarify()
	def export(self, fname = "comics.csv"):
		lst = self.comic_data
		results = []
		headers = list(lst[0].keys())
		results.append(headers)

		for i in lst:
			results.append(S_format(i).d_sort(headers))
		w_csv(results, fname)
		return results


	def standardize_keys(self):
		#normalizes raw data as stored in r_data
		self.import_r_data()
		old = self.r_data
		new = []
		for i in old:
			if int(i.get("CATEGORY")) < 4:
				new.append(self.key_standard_s(i))
		self.comic_data = new
		return new

	def key_standard_s(self, x):
		#accepts dict and produces one with the correct key
		d = {}
		d["Product Name"] = self.text_fix(x.get("FULL_TITLE", "N/A"))
		d["Series Code"] = x.get("SERIES_CODE")
		d["STOCK NO"] = x.get("STOCK_NO")
		d["Issue"] = x.get("ISSUE_NO")
		d["MSRP"] = x.get("SRP")
		d["Publisher"] = self.text_fix(x.get("PUBLISHER"))
		d["Barcode"] = x.get("UPC_NO")
		if d["Barcode"] == " ":
			d["Barcode"] = x.get("EAN_NO")
		d["EAN"] = x.get("EAN_NO")
		d["ISBN"] = x.get("SHORT_ISBN_NO")
		d["Publication Year"] = x.get("PRNT_DATE").split('/')[len(x.get("PRNT_DATE").split('/')) - 1]
		d["DIAMD NO"] = x.get("DIAMD_NO")
		d["Print Date"] = x.get("PRNT_DATE")
		d["Ship Date"] = x.get("SHIP_DATE")
		d["Genre"] = self.genre_trans(x.get("GENRE", ''))
		d["Description"] = self.get_description(x.get("DIAMD_NO"))
		d["Category"] = self.get_cat(x.get("CATEGORY"))
		d["Page Count"] = x.get("PAGE")
		d["Brand Code"] = x.get("BRAND_CODE")
		d["Writer"] = x.get("WRITER")
		d["Artist"] = x.get("ARTIST")
		d["Cover Artist"] = x.get("COVER_ARTIST")
		d["Colorist"] = x.get("COLORIST")
		d["Product Image"] = x.get("STOCK_NO") + ".jpg"
		d["Product Image Link"] = self.dwnld_image(x.get("STOCK_NO"))
		#fixes product name
		d["Product Name"] = self.p_name_fix(d)
		return d
	def dupe_check(self):
		for i in self.comic_data:
			#res = self.cat_obj.query("SELECT " i["DIAMD_NO"]
			pass
		pass

	def p_name_fix(self, x):
		#takes dict, if product name is already in catalog it adds diamond number to the name
		if self.cat_obj.is_in_cat("name", x["Product Name"], '2575'):
			#print("FOUND DUPLICATE")
			new_name = x["Product Name"] + " (" + x.get("DIAMD NO", str(time.localtime()[0])) + ")"
			return new_name
		else:
			return x["Product Name"]
	def get_description(self, x):
		for i in self.preview_data:
			if i["DIAMD_NO"] == x:
				return i["Description"]
	def get_cat(self, x):
		if not x:
			return ''
		return self.cat_dict[str(x)]



	def genre_trans(self,x):
		#takes string and returns the appropriate genre
		if not x:
			#if x is empty string it will return x as empty string
			return ''
		return self.genre_dict.get(str(x), str(x))
	def text_fix(self, x):
		x = str(x).title()
		x = str(x).replace(' Hc ', " HC ")
		x = str(x).replace('Dc ', "DC ")
		x = str(x).replace('Nd ', 'nd ')
		x = str(x).replace('Ii ', 'II')

		x = x.replace("'S", "'s")
		x = re.sub("\(C: \d-\d-\d\)", '', x)
		x = re.sub("\(C: \d-\d-\d", '', x)
		return x

	def dwnld_image(self, x):
		new_s = ''
		for i in x:
			if i.isdigit():
				new_s += i
		start, end = self.comic_image_format(new_s)
		if 'STK' in x:
			prefix =  'STK'
		else:
			prefix = 'STL'


		url = "http://www.previewsworld.com/catalogimages/STK_IMAGES/{3}{1}-{2}/{0}.jpg".format(x, str(self.zero_lead(start)), str(self.zero_lead(end)), prefix)

		return url






	def zero_lead(self, x, length=6):
		while len(str(x)) != length:
			x = '0' + str(x)
		return str(x)
	def comic_image_format(self, x):
		num = int(x)
		for i in range(1, num, 20000):
			if i + 20000 >= num:
				print("Found interval: It is {0} - {1}".format(i, i+19999))
				return i, i+19999

if __name__ == "__main__":
	comic_image_format(sys.argv[1])
