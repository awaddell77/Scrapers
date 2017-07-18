#category selector

class CatSelect:
    def __init__(self, productName):
        self.productName = productName
        self.category = '1361'
        self.rpgCatLst = []

    def keywordSelect(self):
        #uses presence of key word or phrase in product name to descide on category
        pass
    def rpgSelect(self, manufacturer='Other'):
        if manufacturer == "Other":
            return '2761'
