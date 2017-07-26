#category selector
from CatSelect import *
class UnivSelect(CatSelect):
    def __init__(self, productName):
        super().__init__(productName)
        self.spCards = {'HOCKEY TRADING CARDS': '2725', 'BASEBALL TRADING CARDS':'2722',
        'FOOTBALL TRADING CARDS':'2780','MISC. SPORTS CARDS':'2726','NON-SPORTS TRADING CARDS':'2724'}
        self.bgFilter = ['BROKEN TOKEN'] #univ distribution often mistakenly identifies board game accessories as stand alone board games, this list contains publishers that make accessories for board games
        self.rpgs = ['MODIPHIUS', 'ATLAS GAMES']
        self.rpgCats = {'ATLAS GAMES':'6273', 'CATALYST GAMES':''}
        self.category = ''

    def keywordSelect(self):
        #uses presence of key word or phrase in product name to descide on category
        pass
    def select(self, univCat1, univCat2):
        #uses categorization provided by Universal Distribution's site
        #for use with universal distribution scrapers
        if "BOARDGAMES" in univCat1 and univCat2 not in self.bgFilter :
            self.category = '1361'
            return
        elif "SPORTS TRADING CARDS" in univCat1:
            if 'SOCCER TRADING CARDS' in univCat2:
                self.category = '2726'
                return
            elif univCat2 not in list(self.spCards.keys()):
                self.category = '2726'
                return
            self.category = self.spCards[univCat2]
            return
        elif "BATTLE FOAM" in univCat2:
            self.category = '2631'
            return
        elif 'ROLE PLAYING GAMES' in univCat1:
            if "CUBICLE 7" in univCat2 and "DOCTOR WHO" in productName:
                self.category = '8943'
                return
            if "CUBICLE 7" in univCat2 and "THE ONE RING" in productName:
                self.category = '8933'
                return
            if "CUBICLE 7" in univCat2 and "PRIMEVAL" in productName:
                self.category = '12943'
                return
            if "CUBICLE 7" in univCat2:
                self.category = '21323'
                return
            if "CATALYST GAMES" in univCat2:
                #leaves category as board games (1361)
                return
            if "MODIPHIUS" in univCat2:
                self.category = "10393"
                return
            if "GOODMAN GAMES" in univCat2:
                self.category  = '12203'
                return
            if "ATLAS GAMES" in univCat2:
                self.category = "6273"
                return
            if "MISC. RPG" in univCat2:
                self.category = "2761"
                return
            else:
                self.category = "2761"
                return
        elif 'LICENSED GOODS & MEMORABILIA' in univCat2:
            self.category = '7433'
            return
        elif 'DECK PROTECTORS' in univCat2:
            self.category = '1447'
            return
        elif 'PLAYMATS' in univCat2:
            self.category = '1450'
            return
test = UnivSelect("CONAN: ADVENTURES DELUXE CONQUEROR'S EDITION RPG")
test.select("ROLE PLAYING GAMES","MODIPHIUS")
print(test.category)
