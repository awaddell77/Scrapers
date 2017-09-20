#script for warhammer changes
from dictionarify import *
from Cat_dbase import *

class WhCat:
    def __init__(self, fname =''):
        self.data = dictionarify(fname)
        self.catObj = Cat_dbase()
    def moveProduct(self, p_id, cat_id):
        #updates category_id descriptor for product
        self.catObj.update_product(p_id, "category_id", cat_id)
    def moveProducts(self):
        for i in range(0, len(self.data)):
            self.moveProduct(self.data[i]['Product Id'], self.data[i]['Category'])
        print("Done")
    def setData(self, x):
        self.data = dictionarify(x)
