#generates products for magic sealed

class Magic_sealed:
	def __init__(self, name):
		self.name = name
		self.languages =  ["English", "Chinese Simplified", "Chinese Traditional", "French", "German", "Italian", 
		"Japanese", "Korean", "Portuguese", "Russian", "Spanish"]
		self.product_types = ["Booster Box", "Booster Pack"]
		self.m_results = [["Product Name", "Product Image"]]
		self.cat = ""
	def gen_items(self):
		for types in self.product_types:
			full_row = []
			if types == "Booster Box":
				self.cat = "433"
			elif types == "Booster Pack":
				self.cat = "434"

			for i in self.languages:
				full_row = []
				new = self.name + " " + types + " - " + str(i)
				full_row.append(new)
				full_row.append(self.cat)
				self.m_results.append(full_row)
		return self.m_results


