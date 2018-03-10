#difference identifier for lists of dictionaries or other objects
from r_csv_sa import *
class diffId:
    def __init__(self, masterLst, lst):
        self.masterLst = masterLst
        self.lst = lst
        self.data = []
        self.crit = set()
    def check(self):
        for i in self.lst:
            if i not in self.masterLst:
                self.data.append(i)
                self.addToCrit(list(i.keys()))
        if self.data: print("Found {0} new items.".format(len(self.data)))
        else: print("Found no new items.")
    def addToCrit(self, x):
        for i in x: self.crit.add(i)

def test(f1, f2):
    mLst = R_csv(f1).dictionarify()
    lst = R_csv(f2).dictionarify()
    d = diffId(mLst, lst)
    d.check()
    return d.data
