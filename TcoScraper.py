#http://www.tradecardsonline.com scraper
from soupclass8 import *
import time
import sys
class TcoScraper:
    def __init__(self, url):
        self.url = url
        self.mResults = [[]]
        self.browser = ''
        self.links = []
        self.masterCrits = set()
        self.cardList = []
        self.defaultImage = 'no-image.jpg'
    def main(self):
        self.browser = Sel_session('http://www.tradecardsonline.com/')
        self.browser.go_to(self.url)
        time.sleep(2)
        while True:
            self.links += self.link_collector()
            if self.browser.driver.execute_script("return document.getElementsByClassName('padded')[1].children[1].children[0] == null"):
                break
            else:
                self.browser.driver.execute_script("document.getElementsByClassName('padded')[1].children[1].children[0].click()")
        self.mainCust()
    def mainCust(self):
        for i in self.links:
            print("Processing {0}".format(str(i[1])))
            self.splitter(i)
        self.critExtract()
        mCrits = list(self.masterCrits)
        self.mResults.append(self.headerFix(mCrits))
        for cards in self.cardList:
            self.mResults.append(S_format(cards).d_sort(mCrits))
        w_csv(self.mResults,"tcocards.csv")
        self.browser.close()
        return self.mResults




    def critExtract(self):
        self.masterCrits = set()
        for i in self.cardList:
            descriptors = list(i.keys())
            for crit in descriptors:
                self.masterCrits.add(crit)

    def headerFix(self, x):
        return x

    def link_collector(self):
        res = []
        site = self.browser.source()
        links_raw = site.find_all('a', {'target':'card_info'})
        for i in links_raw:
            link = "http://www.tradecardsonline.com" + S_format(str(i)).linkf('<a href=')
            cardName = i.text
            res.append([link, cardName])
        return res


    def splitter(self, x):
        #takes url to card page, returns dictionary
        site = S_base(x[0]).soupmaker()
        table = site.find('div', {'id':'main_card_content'}).table
        image_raw = table.find('a', {'target':'_blank'}).img
        #if image_raw is None: image_raw = '/' + self.defaultImage
        image = S_format(str(image_raw)).linkf('src=')
        imageLink = 'http://www.tradecardsonline.com' + self.urlExtractor(image) + '/big' + image

        data = self.cust_splitter(table)
        data["Card Name"] = x[1]
        data["Product Image"] = image
        data["Image Link"] = imageLink
        self.cardList.append(data)
    def cust_splitter(self, x):
        d = {}
        d['Card Text'] = x.find('p').text
        table = x.find('ul')
        rows = x.find_all('li')
        for i in rows:
            crit = i.strong.text
            i.strong.decompose()
            val = str(i.text).strip(' ')
            d[crit] = val
        return d
    def urlExtractor(self, x):
        #returns the url without the target file on the end
        xLst = x.split('/')
        return '/'.join(xLst[:len(xLst)-1])


if __name__ == "__main__":
    mInst = TcoScraper(sys.argv[1])
    mInst.main()

#test = TcoScraper('http://www.tradecardsonline.com/im/selectCard/card_id/117792/cards_lang/1')
test = TcoScraper('http://www.tradecardsonline.com/?action=searchCards&game_id=57&filter_series_id=890&filter_name=&filter_type_id=&filter_rarity=&filter_number=&filter_text=&goal=&collection_type=&cards_lang=&sort=ca&filter_cost=&filter_strength=&filter_col_02=&filter_subtype_id=&full_format=0&page=1')
testLinks = test.main()
