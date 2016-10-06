from soupclass8 import *
import sys, time

crit = ["Primary Name", 'BGID',"Year Published", "Publisher", "Publishers", "Product Image", "Image Link"]
site_1 = Sel_session()
def main(x):
	urls = text_l(x)
	time_start = time.clock()
	results = [["Product Name", "BGID", "Year", "Publisher", "Publishers", "Product Image", "Image Link", "Ages", "Artist", "Category", "Designer", "Family", "Mechanics", "Players", "Primary Name", "Product Title", "Time"]]
	for i in range(0, len(urls)):
		results.append(splitter(urls[i]))
	w_csv(results, 'BG.csv')
	site_1.close()
	print("Process took %d seconds" % (time.clock()))
	return results



def splitter(x):
	url = x + "/credits"
	site_1.go_to(url)
	site = site_1.source()

	rows = site.find_all('li', {'class':'outline-item'})
	d = {}
	d["BGID"] = url.split('/')[4]
	image_link_r = site.find('img',{'class':'img-responsive'})
	image_link = S_format(str(image_link_r)).linkf('ng-src=')
	image = fn_grab(image_link)
	d["Image Link"] = "http:" + image_link
	d["Product Image"] = image
	for i in range(0, len(rows)):
		cat = rows[i].find('div',{'class':'outline-item-title outline-item-title-lg'}).text
		desc = rows[i].find('div', {'class':'outline-item-description'}).text
		d[cat.strip()] = desc.strip()
	return S_format(d).d_sort(crit)

if len(sys.argv) > 1:
	if sys.argv[1] == '-t':
		splitter(sys.argv[2])
	elif sys.argv[1] == '-m':
		main(sys.argv[2])
else:
	print("URL")



