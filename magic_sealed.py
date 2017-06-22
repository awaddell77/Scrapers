#generates products for magic sealed
import sys
from w_csv import *
class Magic_sealed:
	def __init__(self, name):
		self.name = name
		self.languages =  ["English", "Chinese Simplified", "Chinese Traditional", "French", "German", "Italian", 
		"Japanese", "Korean", "Portuguese", "Russian", "Spanish"]
		self.product_types = ["Booster Box", "Booster Pack", "Booster Case (6 boxes)", "Complete Set", "Complete Set - Foil", 
		"Complete Set of Commons/Uncommons", "Complete Set of Commons/Uncommons - Foil", "Complete Set of Commons/Uncommons x 4 - Foil" ,
		"Complete Set x 4","Complete Set x 4 - Foil", "Complete Set (Without Mythics)","Complete Set - Foil (Without Mythics)",
		"Complete Set of Commons/Uncommons x 4","Complete Set (Without Mythics) x4"]

		self.m_results = [["Product Name", "Product Image", "Category"]]
		self.cat = ""
	def gen_items(self):
		for types in self.product_types:
			full_row = []
			if types == "Booster Box":
				self.cat = "433"
			elif types == "Booster Pack":
				self.cat = "434"
			elif "Complete Set" in types:
				self.cat = "2393"
			else:
				self.cat = ""

			if "Complete Set" not in types and types != "Booster Case (6 boxes)":
				for i in self.languages:
					full_row = []
					new = self.name + " " + types + " - " + str(i)
					full_row.append(new)
					full_row.append("mtg-logo.jpg")
					full_row.append(self.cat)
					self.m_results.append(full_row)
			else:
				full_row = []
				new = self.name + " " + types
				full_row.append(new)
				full_row.append("mtg-logo.jpg")
				full_row.append(self.cat)
				self.m_results.append(full_row)

		return self.m_results


if __name__ == "__main__":
	m_inst = Magic_sealed(sys.argv[1])
	results = m_inst.gen_items()
	w_csv(results, "magic_sealed.csv")
	print("Done")
