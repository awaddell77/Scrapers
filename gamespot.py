from soupclass8 import *
class Gamestop:
	def __init__(self, start_url):
		self.start_url = start_url


	def splitter(self, url):
		site = S_base(url).soupmaker()
		publisher = site.find('h1', {'itemprop':'name'}).cite.text
		publisher = publisher.replace('\n', '')
		publisher = publisher.replace('by ', '')
		publisher = publisher.strip(' ')
		#removing publisher tag from name
		site.find('h1', {'itemprop':'name'}).cite.decompose()
		#name
		name = site.find('h1', {'itemprop':'name'}).text.strip(' ')
		image_link = site.find('div', {'class':'boxart ats-prodBonus-boxArt'}).img
		image_link = "http://www.gamestop.com" + S_format(str(image_link)).linkf("src=")
		#print(str(image_link))
		rating = site.find('a', {'class': 'ats-prodRating-image'}).img
		print(str(rating))
		rating = S_format(str(rating)).linkf('<img alt=')
		return (name, publisher, rating)
test = Gamespot('')
res = test.splitter('http://www.gamestop.com/nintendo-switch/games/has-been-heroes/141915')



