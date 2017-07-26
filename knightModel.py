#knight models scrapers
from Sel_session import *
from soupclass8 import cleaner, fn_grab
from S_format import *
import time
class KnightModel:
    def __init__(self, sUrl):
        self.sUrl = sUrl
        self.mResults = []
        self.browser = ''
        self.allCats = False
        self.getAll = False
    def autoLinkCollector(self, url):
        links = []
        self.browser.go_to(url)

        while True:
            time.sleep(1)
            links += self.linkCollector(self.browser.source(), url)
            if self.browser.driver.execute_script("return document.getElementsByClassName('PagerSizeContainer').length == 0"): break
            button = self.browser.driver.execute_script(
                "return document.getElementsByClassName('PagerSizeContainer')[0].children[document.getElementsByClassName('PagerSizeContainer')[0].children.length - 1].getAttribute('class') == 'Disabled'")
            if button:
                break
            else:
                self.browser.driver.execute_script(
                    "document.getElementsByClassName('PagerSizeContainer')[0].children[document.getElementsByClassName('PagerSizeContainer')[0].children.length - 1].children[0].click()")
        return links
    def main(self, url):
        if self.getAll: links = self.mlinkCollector(url)
        else: links = self.autoLinkCollector(url)
        for i in links:
            self.browser.go_to(i)
            self.mResults.append(self.splitter(self.browser.source()))
        #self.mResults = links

        return self.mResults

    def start(self):
        self.browser = Sel_session()
    def linkCollector(self, x, baseUrl):
        results = []
        base = baseUrl.split('?')[0]
        linkElements = x.find_all('div',{'class':'InfoArea'})
        for i in linkElements:
            link = S_format(str(i.find('h3').a)).linkf('<a href=')
            linkFinal = base + link
            results.append(linkFinal)
        return results
    def mlinkCollector(self, x):
        #grabs links to categories from parent category
        #e.g. it would retrieve the links to all the subcategories in the batman mniniatures game
        linksTotal = set() #set is used to filter out duplicate links
        links1 = []
        self.browser.go_to(x)
        linksPage = self.browser.source()
        links = self.linkCollector(linksPage, x)
        #count = 0 #for testing only
        for i in links:
            #fetches links for all sub categories
            #e.g. https://knightmodels-store.com/epages/afaa2a23-c31d-4ae6-b1cd-12757513fd3b.sf/en_GB/?ObjectPath=/Shops/afaa2a23-c31d-4ae6-b1cd-12757513fd3b/Categories/%22Batman%20Miniature%20Game%22/Escenografia
            self.browser.go_to(i)
            #siteSource = self.browser.source()
            links1 += self.autoLinkCollector(str(i))
        for i in links1: linksTotal.add(i)
        return list(linksTotal)




    def splitter(self, x):
        site = x
        info = site.find('div', {'class':'ProductDetails'})
        name = cleaner(info.find('h1', {'itemprop':'name'}).text, ['\n', '\t', '\r'])
        name = name.replace('\xb4', "'")
        imageInfo = site.find('div', {'class':'ProductImage'}).find('img')
        imageLink = 'https://knightmodels-store.com' + S_format(str(imageInfo)).linkf('data-src-l=')
        imageName = fn_grab(imageLink)
        return [name, imageLink, imageName]

test = KnightModel('')
test.start()
test.getAll = True
#res = test.main('https://knightmodels-store.com/epages/afaa2a23-c31d-4ae6-b1cd-12757513fd3b.sf/en_GB/?ObjectPath=/Shops/afaa2a23-c31d-4ae6-b1cd-12757513fd3b/Categories/%22Batman%20Miniature%20Game%22/Joker')
#res = test.mlinkCollector('https://knightmodels-store.com/epages/afaa2a23-c31d-4ae6-b1cd-12757513fd3b.sf/en_GB/?ObjectPath=/Shops/afaa2a23-c31d-4ae6-b1cd-12757513fd3b/Categories/%22Batman%20Miniature%20Game%22')
res = test.main('https://knightmodels-store.com/epages/afaa2a23-c31d-4ae6-b1cd-12757513fd3b.sf/en_GB/?ObjectPath=/Shops/afaa2a23-c31d-4ae6-b1cd-12757513fd3b/Categories/%22Batman%20Miniature%20Game%22')
test.browser.close()
if __name__ == "__main__":
    mInst = KnightModel('')
    if sys.argv[1] == "-sp":
        mInst.getAll = False
        results = mInst.main(sys.argv[1])
        w_csv(results, "batman_minis.csv")
    elif sys.argv[1] == "-all":
        mInst.getAll = True
        mInst.main(sys.argv[1])
    else:
        print("[-sp /-all] [url]")
