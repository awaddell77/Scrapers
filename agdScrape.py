#scraper for AGD
from Sel_session import *
from soupclass8 import S_format
import time
from cleaner import *
import requests
from Im_dwnld2 import *
class AgdScrape:
    def __init__(self, target_url="https://retailerservices.alliance-games.com/"):
        self.target_url = target_url
        self.browser = ''
        self.image_dir = "C:\\Users\\Owner\\Scrapers\\AGD Images\\"
        self.results = []
    def start(self):
        self.browser = Sel_session(self.target_url)
        self.browser.start()
    def main(self, url):
        self.results += self.scrape_links(url)
        for i in self.results:
            if i["Image Link"]:
                fname = self.image_dwnld(i["Image Link"], cleanFName(i["Product Name"]))
                i["Product Image"] = fname




    def scrape_links(self, x):
        #scrapes links from search result page

        results = []
        links = set()
        self.browser.go_to(x)
        time.sleep(10) #for testing only
        bsObject = self.browser.source()
        res = bsObject.find('div', {'id':'ItemListingGrid'})
        table = res.find('table',{'class':'DiamondGridViewTable ShowThumbnailGridImages'})
        table = table.tbody
        links_raw = table.find_all('a', {'class':'fancybox'})
        links = {"https://retailerservices.alliance-games.com" + S_format(str(i)).linkf('href=') for i in links_raw}
        for i in links:
            results.append(self.scrape_ipage(i))
        return results

    def scrape_ipage(self, x):
        #returns dictionary
        self.browser.go_to(x)
        bsObject = self.browser.source()
        time.sleep(1)
        name = bsObject.find('div',{'class':'Description'}).text
        info = bsObject.find('div', {'class':'ItemDetailData_ColumnContainer'})
        col = info.find_all('div',{'class':'ItemDetailData_ItemLabel'})
        d = {str(i.text).replace(':', ''):cleaner(i.find_next('div', {'class':'ItemDetailData_ItemValue'}).text, ['\n','\t']) for i in col}
        d['Product Name'] = cleaner(name,['\n','\t'])
        image_e = bsObject.find('div',{'class':'ItemDetail_ImageContainer'}).find('a',{'class':'fancyboxImagePopup'})
        if image_e is not None: d["Image Link"] = "https://retailerservices.alliance-games.com" + S_format(str(image_e)).linkf('href=')
        else: d["Image Link"] = ""
        return d
    def dTest(self, x):
        header = {"User-Agent": "Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36"}
        cookies = self.browser.export_cookies()
        s = requests.session()

        s.headers.update(header)
        for i in cookies:
            c_d = {i['name']:i['value']}
            s.cookies.update(c_d)
        return s
    def image_dwnld(self, url,file_name=""):
        img = Im_dwnld2(self.image_dir)
        img.import_cookies(self.browser.export_cookies())
        return img.i_main([url], file_name)
    def cleanFName(self, x):
        s = str(x).replace(' ', '')
        return s






mInst = AgdScrape()
mInst.start()
