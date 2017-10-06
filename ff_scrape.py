
from soupclass8 import *
import sys
from Im_dwnld import *

browser = Sel_session('https://www.fantasyflightgames.com/en/index/')
browser.start()


def main_imp(x, start=0):
	if '.csv' in x:
		urls = r_csv(x)
	else:
		urls = cat_link_grab(x)
	try:
		int(start)
	except ValueError as VE:
		print('Second Argument must be a number')
		return
	for i in range(int(start), len(urls)):
		fname =  urls[i][0] + ".csv"
		main(urls[i][1], re.sub(':', ' -',fname) , re.sub(':', '-', urls[i][0].strip(' ')))
	return "Complete"

def main(x, fname = 'jpokemon.csv', dir_name='Batch Test'):
	links = link_grab(x)
	new = [splitter(links[i]) for i in range(0, len(links))]
	w_csv(new, fname)
	new2 = [new[i][4] for i in range(0, len(new))]
	Im_dwnld(dir_name).i_main(new2)

def cat_link_grab(x):
	browser.go_to(x)
	time.sleep(4)
	wait = WebDriverWait(browser.driver, 10)
	wait.until(EC.element_to_be_clickable((By.CLASS_NAME,'collection-container')))
	site = browser.source()
	cats = site.find('div', {'class':'collection-container'}).find_all('a')
	links = [(cats[i].h3.text, "https://www.fantasyflightgames.com" + S_format(str(cats[i])).linkf('href=')) for i in range(0, len(cats))]
	return links


def link_grab(x):
	browser.go_to(x)
	time.sleep(1)
	wait = WebDriverWait(browser.driver, 10)
	wait.until(EC.element_to_be_clickable((By.ID,'products')))

	site = browser.source()
	links_r = site.find_all('div', {'class':'product-details'})
	new = ["https://www.fantasyflightgames.com" + S_format(str(links_r[i].a)).linkf('<a href=') for i in range(0, len(links_r))]
	return new


def splitter(x):
	#x is the target-level URL
	if type(x) != str:
		print("Argument must be a string")
		return
	browser.go_to(x)
	time.sleep(2)
	wait = WebDriverWait(browser.driver, 10)
	#wait.until(EC.element_to_be_clickable((By.CLASS_NAME,'bx-viewport')))
	wait.until(EC.presence_of_element_located((By.CLASS_NAME,'store-message')))
	site = browser.source()
	print("Now processing %s" % (x))
	try:
		browser.driver.execute_script('return document.getElementsByClassName("product carousel-img-container")[0].innerHTML;')
	except:
		image_link = "https://www.fantasyflightgames.com/static/images/logo_ffgdiamond_blk.png"
		image_name = "No picture found"
	else:
		image_link_r = browser.driver.execute_script('return document.getElementsByClassName("product carousel-img-container")[0].innerHTML;')
		image_link = S_format(image_link_r).linkf('src=')
		image_name = fn_grab(image_link)
	try:
		price = browser.driver.execute_script('return document.getElementsByClassName("store-price ng-binding")[0].innerHTML;')
	except:
		price = "No Price Found"
	name = site.find('h1', {'class':'product-name'})
	t_data = site.find('div',{'id':'technical-data'})
	SKU = next_find(t_data.find(string=re.compile('SKU')))
	ISBN = next_find(t_data.find(string=re.compile('ISBN')))
	return con_text((name, SKU, ISBN)) + (price, image_link, image_name)

def con_text(x):
	#replaces Nones with "Not available"
	if type(x) == tuple:
		new = list(x)
	elif type(x) == list:
		new = x
	else:
		return "Argument must be either tuple or list"
	for i in range(0, len(new)):
		try:
			new[i] = new[i].text
		except AttributeError as AE:
			new[i] = "Not available"
	return tuple(new)
def next_find(x):
	try:
		x.find_next()
	except AttributeError as AE:
		return None
	else:
		return x.find_next()

if len(sys.argv) > 1:
	if sys.argv[1] == '-t':
		print(sys.argv[2])
		splitter(sys.argv[2])
	elif sys.argv[1] == '-s':
		main_imp(sys.argv[2],sys.argv[3])
	elif sys.argv[1] == '-sg':
		main(sys.argv[2], sys.argv[3])
else:
	print("[data]")
