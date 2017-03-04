#GAMA scrape
from soupclass8 import *
site = Sel_session()
site.go_to('http://members.gama.org/directory/search?current_page=1&sort_type=featured&filter={}&asset_type=company_user&display_type=default')
#need to manually log in for security reasons
def link_grab():
	site.go_to('http://members.gama.org/directory/search?current_page=1&sort_type=featured&filter={}&asset_type=company_user&display_type=default')
	results = []
	count = 0
	while True:
		bsObject = site.source()
		links = [["http://members.gama.org" + S_format(str(bsObject.find_all('div', {'class':'member-image'})[i].find('a'))).linkf('<a href=')] for i in range(0, len(bsObject.find_all('div', {'class':'member-image'})))]
		results.extend(links)
		#count += 1
		time.sleep(1)
		if site.driver.execute_script('return document.getElementsByClassName("btn btn-default page")[7].hasAttribute("disabled")'):
			w_csv(results, 'GAMA_contacts.csv')
			return results
		else:
			site.driver.execute_script('document.getElementsByClassName("btn btn-default page")[7].click()')
			time.sleep(1)
def splitter(x):
	site.go_to(x)
	crit = ["Company Name", "Primary Contact:", "Email:", "Phone:", "Website:", "Street Address:", "Address 2:", "City:", "State/Province:", "Country:", "Zip/Postal Code:"]
	d = {}
	bsObject = site.source()
	title = bsObject.h2.text
	d["Company Name"] = title
	table = bsObject.find('table', {'class':'table contact-info-table'})
	rows = table.find_all('tr')
	for i in range(0, len(rows)):
		try:
			d[rows[i].find('td').text] = re.sub('\n', '', rows[i].find('td').find_next('td').text).strip(' ')
		except:
			d[rows[i].find('td').text] = "Not Available"
	return S_format(d).d_sort(crit)





def main(x):
	urls = r_csv(x)
	results = [["Company Name", "Primary Contact:", "Email:", "Phone:", "Website:", "Street Address:", "Address 2:", "City:", "State/Province:", "Country:", "Zip/Postal Code:"]]
	for i in range(0, len(urls)):
		if urls[i][0].split('/')[3] == 'users':
			site.go_to(urls[i][0])
			time.sleep(1)
			bsObject = site.source()
			n_url = 'http://members.gama.org' + S_format(str(bsObject.find('a', {'class':'item_grid_name users-company-name'}))).linkf('href=')
			try:
				results.append(splitter(n_url))
			except:
				results.append([urls[i][0], "Could not find"])
			#else:
				#results.append(splitter(urls[i][0]))
	w_csv(results, 'GAMA_contacts_results.csv')
	return results

