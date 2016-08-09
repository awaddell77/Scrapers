#scraping collectors cache

def splitter(x):
	#scrapes the unique item page
	site = S_base(x).soupmaker()
	if site.find('div', {'id':'ProductImagePane'}).img != None:
		link = 'http://old.collectorscache.com/StoreModules/' + S_format(str(site.find('div', {'id':'ProductImagePane'}).img)).linkf('src=')
		name =  S_format(str(site.find('div', {'id':'ProductImagePane'}).img)).linkf('title=')
		return (name, link)
	else:
		return ("Nothing found for %s") % (x)



