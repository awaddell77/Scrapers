from CatSelect import *

class GtsSelect(CatSelect):
    def __init__(self, productName, publisher = ''):
        super().__init__(productName)
        self.spCards = {'HOCKEY TRADING CARDS': '2725', 'BASEBALL CARDS':'2722',
        'FOOTBALL CARDS':'2780','MISC. SPORTS CARDS':'2726','ENTERTAINMENT CARDS':'2724',
        'BASKETBALL CARDS':'2723'}
        self.cardSleeves = ['DECK PROTECTOR', "SLEEVES"]
        self.playmats = ["PLAYMAT"]
        self.deckBoxes = ["DECK BOX"]
        self.accLst = [self.playmats, self.deckBoxes, self.cardSleeves]
        self.publisher = publisher
        self.category = ''
    def getCategory(self):
        return self.category
    def select(self, cat1):
        #uses categorization provided by GTS's site
        #for use with GTS scrapers
        if "BOARD GAMES" in cat1:
            self.category = '1361'
            return
        elif cat1 in list(self.spCards.keys()):
            self.category = self.spCards[cat1]
            return
        elif "BATTLE FOAM" in cat1:
            self.category = '2631'
            return
        elif 'ROLE PLAYING GAMES' in cat1:
            self.category = self.rpgSelect()

        elif 'TOYS AND FIGURES' in cat1 and "POP!" not in self.productName:
            self.category = '7433'
            return
        if 'FUNKO' in self.publisher and 'TOYS AND FIGURES' in cat1:
            self.category = self.funkoSelect()


        elif cat1 == 'GAMING ACCESSORIES' and "DICE":
            self.category = self.diceParse()
            return

        elif cat1 == "SUPPLIES":
            self.category = self.accSelect()
            return
        else:
            return

    def accSelect(self):
        for i in self.accLst:
            print(i)
            for i_2 in i:
                if i_2 in self.cardSleeves and i_2 in self.productName: return '1447'
                elif i_2 in self.deckBoxes and i_2 in self.productName: return '1451'
                elif i_2 in self.playmats and i_2 in self.productName: return '1450'
        else:
            #returns the category ID for "Other Accessories & Supplies"
            print("{1} is not in {0}".format(self.productName, i_2))
            return '2631'
    def funkoSelect(self):
        if 'Pocket Pop! Keychain' in self.productName: return '13053'
        if "DORBZ" in self.productName: return '12783'
        if 'ROCK CANDY' in self.productName: return '18713'
        else:
            return '21903'






    def diceParse(self):
        #needs to identify manufacturer and then pick the right dice category
        if "DICE BAG" in self.productName or "BAG" in self.productName:
            return "4333"
        else:
            return ""
    def rpgSelect(self):
        if "CUBICLE 7" in self.publisher and "DOCTOR WHO" in self.productName:
            self.category = '8943'
            return
        if "CUBICLE 7" in self.publisher and "THE ONE RING" in self.productName:
            self.category = '8933'
            return
        if "CUBICLE 7" in self.publisher and "PRIMEVAL" in self.productName:
            self.category = '12943'
            return
        if "CUBICLE 7" in self.publisher:
            self.category = '21323'
            return
        if "CATALYST GAMES" in self.publisher:
            #leaves category as board games (1361)
            return
        if "MODIPHIUS" in self.publisher:
            self.category = "10393"
            return
        if "GOODMAN GAMES" in self.publisher:
            self.category  = '12203'
            return
        if "ATLAS GAMES" in self.publisher:
            self.category = "6273"
            return
        else:
            self.category = "2761"
            return ""
