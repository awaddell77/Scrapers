from soupclass8 import *
import os, sys
from Sel_session import *
from linkf import linkF
from Im_dwnld import *
from dictionarify import *
import time
from I_handling import *
from GtsSelect import *

class GtsScrape:
    def __init__(self, url):
        self.url = url
        self.browser = ''
        self.directory = ''
        self.results = []
        self.links = []
        self.pageFix = True
        self.maxPage = '480'
        self.masterCrits = set()
        self.lastExport = []
        self.dir = "GTS Images"
        self.fname = "gts-pos.csv"
        self.crits = ["Product Name", "Category", "Manufacturer SKU", "Manufacturer", "Image Link", "Product Image", "Barcode"]
        self.dImageTog = False
        self.failLst = []
    def main(self):
        self.results = []
        if not self.browser: self.startBrowser()
        self.getLinks()
        n = 1
        for i in self.links:
            print("Working on {0} of {1}. ({2})".format(n, len(self.links), str(i)))
            try:
                self.splitter(str(i))
            except CouldNotLoad as CL:
                print("Could not load page for {0}".format(str(i)))
                n +=1
                self.failLst.append(str(i))
                continue
                #print("Enountered error, trying again")
                #time.sleep(5)
                #self.splitter(str(i))
            n += 1

    def startBrowser(self):
        self.browser = Sel_session("https://www.gtsdistribution.com/")
        self.browser.start()
    def getLinks(self):
        url = self.url
        if self.pageFix and '&rpp=240' not in self.url: url += '&rpp=' + self.maxPage
        self.browser.go_to(url)
        time.sleep(4)
        bsObject = self.browser.source()
        prods = bsObject.find('div',{'id':'prod_listings'})
        links_r = prods.find_all('div', {'class':'prod-thumb'})
        links = [linkF(str(links_r[i].a), 'href=', 'https://www.gtsdistribution.com/') for i in range(0, len(links_r))]
        self.links = links
    def splitter(self, url, tries = 0, tLimit = 2):
        d = {}
        self.goto(url)
        site = self.browser.source()
        try:
            d["Product Name"] = site.find('div', {'class':'page-header detail-title'}).h1.text.replace('\n','')
            table = site.find('div', {'class':'detail-info details'})
            dTable = table.find_all('div', {'class':'title'})
        except AttributeError as AE:
            if tries > tLimit:
                raise CouldNotLoad("Could not load page")
            print("Attribute Error, trying again. Try #{0}".format(str(tries)))
            tries += 1
            self.splitter(url,tries)
            return

        table = site.find('div', {'class':'detail-info details'})
        dTable = table.find_all('div', {'class':'title'})
        for i in range(0, len(dTable)):
            d[cleaner(dTable[i].text, ['\n','\t']).strip()] = cleaner(dTable[i].findNext().text, ["\n", "\t", "\r", "\xa0", "&nbsp;"])
        image_link = site.find('div', {'class':"detail-img-container"})
        image = ''
        if image_link is None: d["Product Image"] = ''
        elif image_link.find('a',{"id":'detail_large'}) is not None: image = linkF(str(image_link.find('a',{"id":'detail_large'})), 'href=',"https://www.gtsdistribution.com/")
        if "no-image" in image: image = linkF(str(image_link.find('a',{"id":'detail_large'})), 'src=',"https://www.gtsdistribution.com/")
        elif image_link.find('a',{"id":'detail_large'}) is None or "no-image.png" in image: image = linkF(str(image_link.find('img',{'id':'prodpicthumb'})), "src=","https://www.gtsdistribution.com/")
        if "no-image" in image: image = ''
        d["Product Link"] = image
        d["Product Image"] = fn_grab(image)
        if image and self.dImageTog:
            dloader = Im_dwnld(self.dir)
            dloader.i_main([image])

        catCategory = GtsSelect(d["Product Name"], d.get("Manufacturer:", 'N/A'))
        catCategory.select(d["Category:"])
        d["Catalog Category"] = catCategory.category
        self.addCrits(d)
        self.results.append(d)
        return
    def addCrits(self, d):
        for i in list(d.keys()): self.masterCrits.add(i)
    def export(self):
        mcrits = ["Product Name", "Catalog Category", "Manufacturer SKU", "Manufacturer", "Category","Image Link", "Product Image", "Barcode"]
        results = [mcrits]
        #crits = list(self.masterCrits)
        crits = ["Product Name","Catalog Category","SKU:","Manufacturer:", "Category:","Product Link", "Product Image", "UPC EACH:"]
        #results.append(crits)
        for i in range(0, len(self.results)):
            results.append(S_format(self.results[i]).d_sort(crits))
        w_csv(results,self.fname)
        self.lastExport = results

        

    def goto(self, x):
        try:
            self.browser.go_to_TO(x)
        except CustomTimeoutException as E:
            print("EXCEPTION")
            self.browser.js("window.stop()")
            self.goto(x)
        except:
            print("EXCEPTION")
            self.browser.js("window.stop()")
            self.goto(x)

        else:
            return

class CouldNotLoad(Exception):
    #for when the product info page won't load
    pass


'''mInst = GtsScrape("https://www.gtsdistribution.com/pc_combined_results.asp?search_keyword=&range=preorder_date~[~2018-03-04~2018-03-10~]")
mInst.startBrowser()
time.sleep(3)
mInst.getLinks()'''
#mInst = GtsScrape("https://www.gtsdistribution.com/pc_combined_results.asp?search_keyword=&range=preorder_date~[~2018-03-04~2018-03-10~]")
#mInst.maxPage = '12'
#mInst.main()

if __name__ == "__main__":
    if sys.argv[1] == "-cdir":
        mInst = GtsScrape(sys.argv[2])
        mInst.dir = sys.argv[3]
        mInst.main()
        mInst.export()
        mInst.browser.close()
        if mInst.failLst:
            print("Failed to process the following {0} product:".format(len(mInst.failLst)))
            for i in mInst.failLst: print(i)


    else:
        mInst = GtsScrape(sys.argv[1])
        mInst.main()
        mInst.export()
        mInst.browser.close()
        if mInst.failLst:
            print("Failed to process the following {0} product:".format(len(mInst.failLst)))
            for i in mInst.failLst: print(i)






