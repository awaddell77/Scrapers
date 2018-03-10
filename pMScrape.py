#petsmart.com scraper
from Sel_session import *
from S_format import *
from linkf import *
from w_csv import *
import time
class pMScrape:
    def __init__(self, fname="output.csv"):
        self.fname = fname
        self.browser = Sel_session("https://www.petsmart.com/")
        self.crits = ["Product Name", "Manufacturer SKU","Brand", "Description", "Pet Type","MSRP"]
        self.results = [self.crits]
        self.data = []

    def start(self):
        self.browser.start()
    def restart(self):
        self.browser = ''
        self.browser = Sel_session("https://www.petsmart.com/")
    def main(self):
        self.browser.go_to("https://www.petsmart.com/search/?q=*&ps=undefined")
        time.sleep(5)
        for i in range(0, 6):
            #should be 0,6
            self.browser.js("document.getElementsByClassName('generic-refinements class1 customPet')[0].children[{0}].children[0].click()".format(i))
            petType = self.browser.js("return document.getElementsByClassName('generic-refinements class1 customPet')[0].children[{0}].children[0].getAttribute('data-lid')".format(i))
            time.sleep(5)

            links = self.link_grab()
            #should click "Next" button and collect every single link for the pet type
            #however this version will only grab the first page
            for i in links:
                self.data.append(self.splitter(i, petType))
            self.browser.go_to("https://www.petsmart.com/search/?q=*&ps=undefined")
            time.sleep(5)
    def export(self, fname='petfile.csv'):
        for i in self.data:
            self.results.append(S_format(i).d_sort(self.crits))
        w_csv(self.results, fname)




    def splitter(self, x, petType=""):
        #takes url (x)
        #returns dict containing product info
        d = {}
        self.browser.go_to(x)
        time.sleep(1)
        bsObject = self.browser.source()
        data = bsObject.find('div', {'id':'product-content'})
        d["Brand"] = ''
        d['Manufacturer SKU'] = data.find('span',{'class':'productID'}).text.strip(' ')
        if data.find('span',{'class':'brand-by'}) is not None: d['Brand'] = data.find('span',{'class':'brand-by'}).text.replace('\n', '').strip(' ')
        d["Product Name"] = data.find('h1', {'class':'product-name'}).text.strip(' ')
        d["Description"] = data.find('div', {'class':'product-description'}).text.strip(' ')
        d["Pet Type"] = petType
        d['MSRP'] = data.find('div', {'class':'product-price'}).text.replace('\n','')


        return d
    def link_grab(self):
        bsObject = self.browser.source()
        table = bsObject.find('ul', {'id':'search-result-items'})
        linksRaw = table.find_all('a', {'class':'name-link'})
        links = [linkF(str(linksRaw[i]), 'href=', 'https://www.petsmart.com') for i in range(0, len(linksRaw))]
        return links




mInst = pMScrape()
#mInst.start()
#res = mInst.splitter("https://www.petsmart.com/featured-shops/pick-up-and-save/grreat-choice-dog-crate-19958.html?cgid=60000060")
