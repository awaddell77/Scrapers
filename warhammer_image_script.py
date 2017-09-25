#script for warhammer changes
from dictionarify import *
from Cat_dbase import *
from w_csv import *

class WhCat:
    def __init__(self, fname =''):
        self.data = dictionarify(fname)
        self.catObj = Cat_dbase()
        self.mResults = []
        self.csvData = []
    def moveProduct(self, p_id, cat_id):
        #updates category_id descriptor for product
        self.catObj.update_product(p_id, "category_id", cat_id)
    def moveProducts(self):
        for i in range(0, len(self.data)):
            self.moveProduct(self.data[i]['Product Id'], self.data[i]['Category'])
        print("Done")
    def setData(self, x):
        self.data = dictionarify(x)
    def barcodeImages(self):
        p_ids = self.catObj.get_prod_by_ptype('1122')
        results = []
        idPictures = []
        tCount = 0
        for i in p_ids:
            #print(i)#remove after testing
            results.append(self.catObj.get_product(i[0]))
            #tCount += 1
            #if tCount > 25: break
            print(".", end = "", flush = True)
        print("\n")
        for i in range(0, len(results)):
            res = self.catObj.query("SELECT photo_file_name, id FROM products WHERE barcode = \"{0}\";".format(results[i]["GW Barcode"]))
            print(results[i])
            print(res)
            print(type(res))
            results[i]["New Image"] = ''
            results[i]["New Image Link"] = ''
            if res and res[0][0] is not None:
                results[i]["New Image"] = res[0][0]
                results[i]["New Image Link"] = "https://crystalcommerce-assets.s3.amazonaws.com/photos/" + str(res[0][1]) + '/' + str(results[i]["New Image"])
        self.mResults = results
        nRes = [(results[i]['id'], results[i]['New Image'], results[i]['New Image Link']) for i in range(0, len(results))]
        self.csvData = nRes
        return results

test = WhCat('gw_trade.csv')
