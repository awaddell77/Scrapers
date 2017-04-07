#item creation for amazon
from soupclass8 import *

browser = Sel_session("https://sellercentral.amazon.com/gp/homepage.html")
browser.start()
test_card = {'Product Name':"This is the card's name", 'Manufacturer': 'The Pokémon company', 'Ages':"12", 'Barcode':'0642645120110',
				"Barcode Type": 'upc', "Product Id":'6339605', "MSRP":'2.10', 'Product Image': 'pkm-cardback.png', "Description":'This is the description',
				"Keywords":"kids"}
class Asin_Add_Main(object):
	def __init__(self, p_list, dir_n ="C:\\Users\\Owner\\Desktop\\I\\", *args):
		self.dir_n = dir_n
		self.p_list = conv_to_dict(p_list, self.dir_n)
		self.args = args
		self.header = r_csv_2(p_list, mode = 'rb', encoding = 'ISO-8859-1' )[0]
		self.asins = []
	def get_asins(self):
		return self.asins
	def clear_asins(self):
		self.asins = []

	def add_single(self, x, dir_n = "C:\\Users\\Owner\\Desktop\\I\\" ):
		n = 0
		browser.go_to("https://catalog.amazon.com/abis/Classify/SelectCategory?itemType=collectible-single-trading-cards&productType=TOYS_AND_GAMES")
		#name
		browser.js("document.getElementById('item_name').value = '{0}'".format(prep(x["Product Name"])))
		#manufacturer
		browser.js("document.getElementById('manufacturer').value = '{0}'".format(prep(x["Manufacturer"])))
		#brand name
		browser.js("document.getElementById('brand_name').value = '{0}'".format(prep(x["Manufacturer"])))
		#minimum age
		browser.js("document.getElementById('mfg_minimum').value = '{0}'".format(prep(x["Ages"])))
		#minimum age units
		browser.js("document.getElementById('mfg_minimum_unit_of_measure').value = '{0}'".format("years"))
		#barcode
		browser.js("document.getElementById('external_product_id').value = '{0}'".format(prep(x["Barcode"])))
		#barcode type
		browser.js("document.getElementById('external_product_id_type').value = '{0}'".format(prep(x["Barcode Type"])))
		#clicks over to Offer tab
		browser.js("document.getElementById('offer-tab').click()")
		time.sleep(1)
		#SKU
		browser.js("document.getElementById('item_sku').value = '{0}'".format(x["Product Id"]))
		#condition
		browser.js("document.getElementById('condition_type').value = 'collectible, like_new'")
		#MSRP
		browser.js("document.getElementById('standard_price').value = '{0}'".format(x["MSRP"]))
		#Quantity
		browser.js("document.getElementById('quantity').value = '0'")
		#switch over to image tab
		browser.js("document.getElementById('image-tab').click()")
		time.sleep(1)
		#Image
		self.add_image(x["Product Image"], dir_n)
		time.sleep(5)
		#switch over to Description tab
		browser.js("document.getElementById('tang_description-tab').click()")
		time.sleep(1)
		#Add description
		browser.js("document.getElementById('product_description').value = '{0}'".format(prep(x["Description"])))
		#switch over to Keywords tab
		browser.js("document.getElementById('tang_keywords-tab').click()")
		time.sleep(1)
		#adds keyword
		browser.js("document.getElementById('target_audience_keywords1').value = '{0}'".format(prep(x["Keywords"])))
		time.sleep(.5)
		#clicks back on the vital info tab
		browser.js("document.getElementById('tang_vital_info-tab').click()")
		time.sleep(1)

		while not browser.is_enabled("main_submit_button"):
			n += 1
			time.sleep(.5)
			if n >= 20:
				raise Amazon_Validation_Error("Amazon will not validate {0}".format(x["Product Name"]))
		if browser.is_enabled("main_submit_button"):
			#this is for testing only
			browser.js("document.getElementById('main_submit_button').click()")
			print("CLICKED THE SUBMIT BUTTON!")
			load_check_abort = 0
			#has to wait for the page to transition to the seller central page
			while load_check('sellercentral'):
				print("Waiting for sellercentral page")
				load_check_abort += 1
				time.sleep(1)
				if load_check_abort > 30:
					raise RuntimeError("Amazon either took too long to respond or objected to the item.")
			print("Found sellarcentral page")
			return True
		else:
			return False

	def add_image(self, x, dir_n= "C:\\Users\\Owner\\Desktop\\I\\"):
		if "http://" in x:
			x = fn_grab(x)
		x =  dir_n + x

		browser.js("return document.getElementById('Parent-ProductImage_MAIN-div').children[2].getElementsByTagName('input')[10]").send_keys(x)

	def add_csv(self, dir_n = "C:\\Users\\Owner\\Desktop\\I\\"):
		succ_list = [self.header]
		fail_list = [self.header]
		for i in range(0, len(self.p_list)):
			try:
				outcome = self.add_single(self.p_list[i], dir_n)
			except Amazon_Validation_Error as AVE: #untested
				print("Error occurred:")
				print(AVE)
				print("Trying again but with EAN")
				try:
					self.p_list[i]["Barcode Type"] = 'ean'
					outcome = self.add_single(self.p_list[i], dir_n)
				except Amazon_Validation_Error as AVE:
					self.p_list[i] = barcode_handling(self.p_list[i])
					fail_list.append(S_format(self.p_list[i]).d_sort(self.header))

				#self.p_list[i] = barcode_handling(self.p_list[i])
				#fail_list.append(S_format(self.p_list[i]).d_sort(self.header))
			except:
				#general
				self.p_list[i] = barcode_handling(self.p_list[i])
				print("General Error Occurred with {0}".format(self.p_list[i]["Product Name"]))
				fail_list.append(S_format(self.p_list[i]).d_sort(self.header))

			else:
				if outcome:
					succ_list.append(S_format(self.p_list[i]).d_sort(self.header))
				else:
					self.p_list[i] = barcode_handling(self.p_list[i])
					fail_list.append(S_format(self.p_list[i]).d_sort(self.header))

			time.sleep(1)
		w_csv(succ_list, "SUCCESS LIST.csv")
		w_csv(fail_list, "FAILED ADDS.csv")
	def retrieve_asins(self):
		for i in range(0, len(self.p_list)):
			self.asins.append(self.grab_asin(self.p_list[i]["Product Id"]))
		w_csv(self.asins, "ASIN_list.csv")
	def grab_asin(self, name):
		wait = 3
		#retrieves ASIN that has already been created. Need product id.
		#name == Product Id or Item Sku on Amazon 
		#needs to be on the "Manage Inventory" page
		#name = re.sub("'", "39;", name) #used to be \\'
		try:
			int(name)
		except ValueError as VE:
			name = re.sub("'", rep, name)
			if "Foil" not in name:
				name_1 = name + " NOT Foil"
			else:
				name_1 = name
		else:
			name_1 = str(name)

		browser.js("document.getElementById('myitable-search').value ='" + name_1 + "' ;")
		browser.js("document.getElementById('myitable-search-button').children[0].children[0].click();")
		time.sleep(wait)
		site = browser.source()
		#ASIN = browser.js("return document.getElementById('NjIzMjk2Mw_e_e-title-asin').children[0].children[0].innerHTML;")
		try:
			ASIN = re.sub('\n', '', site.find('div', {'data-column':'asin'}).text).strip()
		except TypeError as TE:
			return [name, "No ASIN found"]
		except AttributeError as AE:
			return [name, "No ASIN returned"]
		else:
			return [name, ASIN]

def load_check(start):
	#checks to see if browser has switched to the sellercentral page after clicking on the save button on the item creation page
	if browser.js('return document.readyState') != "complete" or start not in browser.driver.current_url:
		return True
	else:
		return False
def barcode_handling(x):
	d = x 
	d["Barcode"] = '[' + str(d["Barcode"])
	return d


class Crit_not_present(Exception):
	pass
class Value_not_appr(Exception):
	#for when the contents are not appropriate or valid
	pass
class Image_not_found(Exception):
	#for when it cannot find the images
	pass
class Amazon_Validation_Error(Exception):
	pass
def prep(x):
	value = x
	value = re.sub("'", "\\\'",  value)
	value = re.sub('"', '\\\"', value)
	return value
def conv_to_dict(x, dir_n = "C:\\Users\\Owner\\Desktop\\I\\"):
	new_x = dictionarify(x)
	crits = ['Manufacturer', 'Product Image', 'Barcode Type', 'Barcode', 'Product Id', 'MSRP', 'Product Name', 'Description', 'Ages', 'Keywords']
	for i_2 in range(0, len(new_x)):
		#checks to see if Image Link is present if Product Image field is not, then creates a product image field by extracting the file name from the url
		if "Product Image" not in list(new_x[i_2].keys()) and "Image Link" in list(new_x[i_2].keys()):
			new_x[i_2]["Product Image"] = fn_grab(new_x[i_2]["Image Link"])
		for i in range(0, len(crits)):
			#checks each dict to see if they have the necessary fields
			req_field_pres = crits[i] not in list(new_x[i_2].keys())
			missing_crit = ke_check(new_x[i_2], crits[i])
			empty_field = empty_check(new_x[i_2], crits[i])
			if req_field_pres or missing_crit or empty_field:
				if req_field_pres:
					raise Crit_not_present("CSV is missing a required field: {0}".format(crits[i]))
				if missing_crit:
					raise Crit_not_present("Item #{0} is missing a required field: {1}".format(str(i_2), crits[i]))
				if empty_field:
					raise Crit_not_present("The {0} field in item #{1} was left blank.".format(crits[i], str(i_2)))
		#checks to see if fields contain appropriate content (i.e. the correct type of data)
		b_code_er, p_id_er, msrp_er = number_check(new_x[i_2]["Barcode"]), number_check(new_x[i_2]["Product Id"]), number_check(new_x[i_2]["MSRP"])
		if b_code_er or p_id_er or msrp_er:
			if b_code_er:
				raise Value_not_appr("Barcode value {0} for Item #{1} (Product Name: {2}) is invalid".format(new_x[i_2]["Barcode"], str(i_2), new_x[i_2]["Product Name"]))
			if p_id_er:
				raise Value_not_appr("Product Id {0} for Item #{1} (Product Name: {2}) is invalid".format(new_x[i_2]["Product Id"], str(i_2), new_x[i_2]["Product Name"]))
			if msrp_er:
				raise Value_not_appr("MSRP {0} for Item #{1} (Product Name: {2}) is invalid".format(new_x[i_2]["MSRP"], str(i_2), new_x[i_2]["Product Name"]))
		if not image_check(new_x[i_2]["Product Image"], dir_n):
			raise Image_not_found("Image file {0} not found in directory {1}".format(new_x[i_2]["Product Image"], dir_n))
	return new_x





	#would check if the criteria were there and also if they were valid
def ke_check(x, key):
	#returns true for key errors
	try:
		x[key]
	except KeyError as KE:
		return True
	else:
		return False
def empty_check(x, key):
	#returns true if value is empty of '' AND ONLY when that is the case. If there is no such key it returns false anyways
	try:
		contents = x[key]
	except KeyError as KE:
		return False
	else:
		if contents == '':
			return True
		else:
			return False

def number_check(x):
	#checks to see if barcode, product Id, MSRP are numbers. Returns True if error is detected
	try:
		int(x)
	except ValueError as VE:
		try:
			float(x)
		except ValueError as VE:
			return True
		else:
			return False
def image_check(x, dir_n = "C:\\Users\\Owner\\Desktop\\I\\"):
	full_path = dir_n + x
	if os.path.exists(full_path):
		return True
	if not os.path.exists(full_path):
		return False

def run_prog(x):
	x = ''
	accept = ["Yes", 'y', 'Y']
	exit = ["Exit", "q", "Q", 'bye', 'N', 'n']
	while x not in accept or exit:
		x = input("Proceed with program (Y/N)?: ")
		if x == "END":
			break
	if x in accept:
		return True
	else:
		return False





#test_inst = Main('test_adds.csv')

if __name__ == "__main__":
	if sys.argv[1] == '-h':
		print("python3 [prog_name.py] \"[csv file name]\" [-nd] [Full path to new directory for images]")
	else:
		m_inst = Asin_Add_Main(sys.argv[1])
		res = run_prog(1)
		if res and sys.argv[2] == '-nd':
			m_inst.add_csv(sys.argv[3])
		elif res:
			m_inst.add_csv()
		else:
			browser.close()




