#wikia
from soupclass8 import *
import sys

def galleryScrape(x):
    results = [["Card Name", "Card Number", "Rarity"]]
    site = S_base(x).sel_soup()
    table = site.find('div',{'id':'gallery-0'})
    items = table.find_all('div', {'class':'lightbox-caption'})
    for i in items:
        print(i)
        results.append(splitter(i))
    w_csv(results)
def splitter(x):
    #grabs link text, removes it, and then grabs the results
    name = x.a.text
    x.a.decompose()
    numberRarity = x.text
    cardNumber = numberRarity.split(' ')[0]
    cardRarity = numberRarity.split(' ')[1]
    cardRarity = cardRarity.replace('(','')
    cardRarity = cardRarity.replace(')', '')
    cardRarity = cardRarity.strip(' ')
    return [name, cardNumber, cardRarity]

if __name__ == "__main__":
    galleryScrape(sys.argv[1])
