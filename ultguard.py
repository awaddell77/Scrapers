#ultimate guard
from soupclass8 import *
def splitter(x):
	site = S_base(x).sel_soup()
	results = []
	title = re.sub('\u2122', ' ', site.find('h1', {'class':'t-article'}).text)
	colors_r = site.find_all('p', {'class':'block-color'})
	colors = [colors_r[i].text for i in range(0, len(colors_r))]
	for i in range(0, len(colors)):
		product_name = [str(title) + ' - ' + str(colors[i]).strip(' ')]
		results.append(product_name)
	return results

test = splitter('http://ultimateguard.com/en/boxes-cases/twin-flip-n-tray/twin-flip-n-tray-deck-case-160-2016/amber.html')

