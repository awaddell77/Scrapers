#star wars destiny program
import requests
from soupclass8 import *
import sys
class SwDestiny:
    def __init__(self, set_code):
        self.set_code = set_code
        self.set_data = []
        self.results = []
        self.header = ["Product Name", "Product Image", "Image Link", "Color", "Affiliation", "Faction", "Card Number", "Rarity", "Health", "Point Values", "Special Abilities", "Set"]
    def get_set(self):

        resp = requests.get("https://swdestinydb.com/api/public/cards/" + self.set_code + ".json")
        data = resp.json()
        self.set_data = data
        return data
    def exportData(self, output="swfile.csv"):
        self.results.append(self.header)
        for i in range(0, len(self.set_data)):
            self.results.append(S_format(self.set_data[i]).d_sort(self.header))
        w_csv(self.results, output)

    def norm_data(self):
        for i in self.set_data:
            i["Faction"] = i.get("faction_name", "")
            i["Color"] = self.color(i["faction_name"])
            i["Product Name"] = i.get("label", "")
            i["Point Values"] = i.get("points", "")
            i["Affiliation"] = i.get("affiliation_name", "")
            i["Card Number"] = i.get("position","")
            i["Rarity"] = i.get("rarity_name","")
            i["Special Abilities"] = i.get("text", "")
            i["Set"] = i.get("set_name", "")
            i["Health"] = i.get("health", "")
            i["Points"] = i.get("points", "")


            if i["imagesrc"] is None:
                i["Product Image"] = "Star-Wars-Destiny-logo.jpg"
                i["Image Link"] = ""
            else:
                i["Product Image"] = fn_grab(i["imagesrc"])
                i["Image Link"] = i["imagesrc"]







    def color(self, x):
        d = {"Force":"Blue","Command":"Red","Rogue":"Yellow","General":"Gray"}
        return d.get(x.strip(" "), x)
#testing
mInst = SwDestiny("LEG")
mInst.get_set()
mInst.norm_data()
if __name__ == "__main__":
    mInst = SwDestiny(sys.argv[1])
