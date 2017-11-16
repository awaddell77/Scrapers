#script for pricecharting images
from soupclass8 import *
import os
from Sel_session import *
from linkf import linkF
from Im_dwnld import *
from dictionarify import *
import time
from Cat_dbase import *
class priceCharting:
    def __init__(self, url="", **kwargs):
        self.url = url
        self.productList = []
        self.tdir = kwargs.get("tdir",os.getcwd())
        self.browser = ''
        self.games = []
        self.results = []
        self.catObj = ''


    def start_browser(self):
        self.browser = Sel_session("https://www.pricecharting.com/")
        self.browser.start()
    def getVGamesData(self, cat = ""):
        self.catObj = Cat_dbase()
        self.catObj.set_proper_desc(True)
        if cat:
            products = self.catObj.query("SELECT id FROM products WHERE product_type_id = \"1125\" AND category_id = \"{0}\";".format(str(cat)))
        else:
            products = self.catObj.query("SELECT id FROM products WHERE product_type_id = \"1125\";")
        #remove limit after testing
        for i in range(0, len(products)):
            #REMOVE THE STEP AFTER TESTING
            print("Processing", str(products[i][0]), "(#{0} out of {1})".format(i, len(products)))
            self.games.append(self.catObj.get_product(products[i][0]))
        self.games.sort(key=sort1)

        print("DONE")




    def imageLinkCollector(self, games):
        #takes list of dicts
        dLoader = Im_dwnld("C:\\Users\\Owner\\Scrapers\\Video Game Images\\")
        for i in games:
            name = self.nameFix(i["Product Name"])
            print("Attempting to process {0}".format(i["Product Name"]))
            console = self.consoleFix(i["Console"])
            url = "https://www.pricecharting.com/game/" + console + "/" + name
            self.browser.go_to(url)
            linkInitial = "https://www.pricecharting.com" + self.splitter(self.browser.source())
            print("linkInitial: " + linkInitial)
            self.browser.go_to(linkInitial)
            time.sleep(.5)
            imageElement = self.browser.source()
            imageLink = self.splitter2(imageElement)
            print("imageLink: " + imageLink)
            if "no-image-available" not in imageLink:
                fname = dLoader.d_img(imageLink, str(i["Product Id"]))
                i["Product Image"] = fname
            else:
                i["Product Image"] = ""
        return games
    def goto(self, x):
        try:
            self.browser.go_to(x)
        except CustomTimeoutException as E:
            self.browser.js("window.stop()")
            self.browser.go_to(x)
    def export(self, output="vg_export.csv"):
        self.results = []
        keys = list(self.games[0].keys())
        self.results.append(keys)
        for i in self.games:
            self.results.append(S_format(i).d_sort(keys))
        w_csv(self.results, output)





    def nameFix(self, s):
        s1 = str(s).split(" ")
        s1 = "-".join(s1)
        s1 = s1.replace(".","")
        return s1
    def consoleFix(self, s):
        s1 = str(s).lower()
        s1 = s1.split(" ")
        s1 = "-".join(s1)
        return s1

    def main_s(self, x):
        bsObject = S_base(x).sel_soup()
        return self.splitter(bsObject)
    def import_csv(self, fname):
        self.games = dictionarify(fname)





    def splitter(self, x):
        #takes BeautifulSoup bsObject
        #returns image link

        cover = x.find('div', {'class':'cover'})
        img_element = cover.find("img")
        link = S_format(str(img_element)).linkf("src=")
        return link
    def splitter2(self, x):
        imageElement = x.img
        imageLink = S_format(str(imageElement)).linkf("src=")

        return imageLink
def sort1(x):
    return x["Console"]

mInst = priceCharting()
mInst.getVGamesData("22381")
mInst.start_browser()
mInst.browser.timeout = True
results = mInst.imageLinkCollector(mInst.games)
'''mInst.start_browser()
mInst.browser.timeout = True
mInst.import_csv("video_test.csv")
results = mInst.imageLinkCollector(mInst.games)
mInst.export()'''

if __name__ == "__main__":
    h = priceCharting(sys.argv[1])
