#script for pricecharting images
from soupclass8 import *
import os, sys
from Sel_session import *
from linkf import linkF
from Im_dwnld import *
from dictionarify import *
import time
from Cat_dbase import *
from I_handling import *
class priceCharting:
    def __init__(self, url="", **kwargs):
        self.url = url
        self.productList = []
        self.tdir = kwargs.get("tdir",os.getcwd())
        self.browser = ''
        self.games = []
        self.results = []
        self.catObj = ''
        self.skippedLst = []
        self.timeout = 10
        self.timeoutToggle = True
        self.nonJ = False
    def main(self, cats = [], limit = 0, fname = "vg_export.csv"):
        self.games = []
        if not cats:
            self.getVGamesData("", limit)
        elif isinstance(cats, (str, int)): cats = [cats]
        for i in cats:
            self.getVGamesData(i)
        self.start_browser()
        self.browser.timeout = self.timeoutToggle
        time.sleep(1)
        self.imageLinkCollector(self.games)
        self.export(fname)







    def start_browser(self):
        self.browser = Sel_session("https://www.pricecharting.com/")
        self.browser.start()
        self.browser.driver.set_page_load_timeout(self.timeout)
    def getVGamesData(self, cat = "", limit = 0):
        self.catObj = Cat_dbase()
        self.catObj.set_proper_desc(True)
        if cat:
            products = self.catObj.query("SELECT id FROM products WHERE product_type_id = \"1125\" AND category_id = \"{0}\" AND photo_file_name IS null;".format(str(cat)))
        elif self.nonJ:
            products = self.catObj.query("SELECT id FROM products WHERE product_type_id = \"1125\" AND photo_file_name IS null AND category_id NOT IN (\"22334\", \"22335\",\"22336\",\"22377\");".format(str(cat)))
        else:
            products = self.catObj.query("SELECT id FROM products WHERE product_type_id = \"1125\" AND photo_file_name IS null;")
        if limit > 0: end = limit
        else: end = len(products)
        for i in range(0, end):
            print("Processing", str(products[i][0]), "(#{0} out of {1})".format(i+1, end))
            self.games.append(self.catObj.get_product(products[i][0]))
        self.games.sort(key=sort1)

        print("DONE")




    def imageLinkCollector(self, games):
        #takes list of dicts
        tdir = "C:\\Users\\Owner\\Scrapers\\Video Game Images\\"
        dLoader = Im_dwnld(tdir)
        count = 0
        for i in games:
            name = self.nameFix(i["Product Name"])
            count += 1
            print("Attempting to process {0} (#{1} of {2})".format(i["Product Name"], count, len(games)))
            console = self.consoleFix(i["Console"])
            url = "https://www.pricecharting.com/game/" + console + "/" + name
            self.goto(url)
            try:
                linkInitial = "https://www.pricecharting.com" + self.splitter(self.browser.source())
            except AttributeError as AE:
                self.skippedLst.append(i)
                print("SKIPPED {0}".format(i["Product Name"]))
                continue
            print("linkInitial: " + linkInitial)
            self.goto(linkInitial)
            time.sleep(.5)
            imageElement = self.browser.source()
            try:
                imageLink = self.splitter2(imageElement)
            except AttributeError as AE:
                self.skippedLst.append(i)
                print("SKIPPED {0}".format(i["Product Name"]))
                continue
            print("imageLink: " + imageLink)
            if "no-image-available" not in imageLink:
                fname = dLoader.d_img(imageLink, str(i["Product Id"]))
                i["Product Image"] = fname

                try:
                    imageF = I_handling(tdir + fname)
                    imageF.resizeByFactor(2.5)
                except TypeError as TE:
                    print("Type Error detected")
                    i["Product Image"] = ""
                except KeyboardInterrupt as KE:
                    break
                except:
                    print("Error detected")
                    print(sys.exc_info()[:])

            else:
                i["Product Image"] = ""
        self.browser.close()
        return games
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
    def export(self, output="vg_export.csv"):
        self.results = []
        #keys = list(self.games[0].keys())
        keys = ["Product Name", "Product Id", "Product Image", "Console", "PCID"]
        self.results.append(keys)
        for i in self.games:
            self.results.append(S_format(i).d_sort(keys))
        w_csv(self.results, output)

    def nameFix(self, s):
        s1 = str(s).replace("/", "")
        s1 = s1.split(" ")
        s1 = "-".join(s1)
        s1 = s1.replace(".","")
        s1 = s1.replace(":", "")
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

#mInst = priceCharting()
#mInst.main('22348')
#mInst.getVGamesData("22384")
#mInst.getVGamesData("22354")

#mInst.start_browser()
#mInst.browser.timeout = True
#results = mInst.imageLinkCollector(mInst.games)
#mInst.export("segamasters.csv")
'''mInst.start_browser()
mInst.browser.timeout = True
mInst.import_csv("video_test.csv")
results = mInst.imageLinkCollector(mInst.games)
mInst.export()'''

if __name__ == "__main__":
    h = priceCharting()

    if "," in sys.argv[1]:
        ids = sys.argv[1].split(",")
        cat_lst = [i.strip() for i in ids]
        h.start_browser()
        h.browser.timeout = True
        h.main(cat_lst)
    else:
        h.start_browser()
        h.browser.timeout = True
        h.main(sys.argv[1])
