#for processing jsons from mtgjson
from loadJson import *
import os, sys, copy, re
from soupclass8 import S_format, w_csv
class MtgParse:
	def __init__(self, fname):
		self.fname = fname
		self.data = {}
		self.set = []
		self.maxNum = None
	def load(self):
		self.data = loadJson(self.fname)
	def getSet(self, set_name):
		self.set = self.data[set_name]['cards']
		return self.set
	def getcrit(self, crit, value, pop=False):
		#searches through set, returns card that has the appropriate value
		for i in range(0, len(self.set)):
			if self.set[i][crit] == value and not pop: return self.set[i]
			elif self.set[i][crit] == value and pop:
				#print("Found {0}".format(self.set[i]['name']))
				return self.set.pop(i)

	def normalize(self):
		for i in self.set:
			#card_number is a copy of number and therefore redundant for most cards except for double-sided ones
			i['card_number'] = i.get('number', '')
			if not i.get('manaCost', ''): i['manaCost'] = ''
			i['manaCost'] = i['manaCost'].replace('{','').replace('}', '')
			if 'Basic Land' in i['type'] and i['card_number']: i['name'] = i['name'] + ' (' + i['number'] + ')'

		maxlen = len(self.set)
		for i in range(maxlen-1, -1, -1):
			if self.set[i].get('number', '').isalnum() and 'a' in self.set[i].get('number', ''):
				print("Combining {0}".format(self.set[i]['name']))
				card_2 = self.getcrit('number', self.set[i]['number'].replace('a', 'b'), True)
				print("Card 2 is: {0}".format(card_2['name']))
				self.combine(self.set[i], card_2)
				#maxlen -= 1
	def foil(self):
		foils = []
		for i in self.set:
			d = copy.deepcopy(i)
			d['name'] = i['name'] + ' - Foil'
			foils.append(d)
		self.set += foils



	def combine(self, card_1, card_2):
		#combines two cards
		#print("Combining {0} and {1}".format(card_1['name'], card_2['name']))
		card_1['name'] = card_1['name'] + ' // ' + card_2['name']
		card_1['number'] = card_1['number'] + ' // ' + card_2['number']
		card_1['text'] = card_1.get('text', '') + ' // ' + card_2.get('text', '')
		card_1['type'] = card_1['type'] + ' // ' + card_2['type']



	def export(self, set_name ='', t_dir=''):
		if set_name: nset = self.getSet(set_name)
		if not t_dir: t_dir = os.getcwd()
		header = ['Name', 'Color', 'Type', 'Cost', 'Artist', "Card Number"]
		crits = ['name', 'colorIdentity', 'type', 'manaCost','artist', 'card_number']
		results = [header]
		for i in range(0, len(self.set)):
			num = re.sub('[a-z]', '', self.set[i]['card_number'])
			if self.maxNum is not None and int(num) <= int(self.maxNum): results.append(S_format(self.set[i]).d_sort(crits))
			elif self.maxNum is None: results.append(S_format(self.set[i]).d_sort(crits))
		w_csv(results, 'mtgset.csv')




def test(x):
	mInst = MtgParse('AllSets.json')
	mInst.load()
	mInst.getSet("XLN")
	mInst.normalize()
	return mInst

if __name__ == "__main__":
	if sys.argv[1] == '-num':
		mInst = MtgParse(sys.argv[3])
		mInst.maxNum = sys.argv[2]
		mInst.load()
		mInst.getSet(sys.argv[4])
		mInst.normalize()
		mInst.foil()
		mInst.export()
	else:
		mInst = MtgParse(sys.argv[1])
		mInst.load()
		mInst.getSet(sys.argv[2])
		mInst.normalize()
		mInst.foil()
		mInst.export()