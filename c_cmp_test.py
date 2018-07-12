from csv_compare import *
#csv_compare test


class Tester:
	def __init__(self, ag_fname, master_fname):
		self.ag_fname = ag_fname
		self.master_fname = master_fname
		self.agencies = ''
		self.master_data = ''
		self.matched = []
		self.matched_2 = []
	def load_origs(self):
		self.agencies = dictionarify(self.ag_fname)
		self.master_data = dictionarify(self.master_fname)
	def transform(self):
		self.agencies = trans_by_co(self.agencies)
		self.master_data = clean(self.master_fname, ['#', '*', '$', '!'])
	def phase_1_test(self):
		self.matched = phase_1(self.agencies, self.master_data)
	def phase_2_test(self):
		self.matched += phase_2(self.agencies, self.master_data)

	def match_status(self):
		print("Size of unmatched agency list/master: {0}/{1}".format(str(len(self.agencies)), str(len(self.master_data))))
		print("Size of matched list: {0}".format(str(len(self.matched))))
	def dupe_count(self):
		d = {}
		count = 0
		for i in self.master_data:
			if d.get(i["Name"], ''): count += 1
			else: d[i["Name"]] = 1
		return count
m_inst = Tester('scl.csv', 'kcl_2.csv')
m_inst.load_origs()
m_inst.transform()
m_inst.match_status()
m_inst.phase_1_test()
m_inst.match_status()
m_inst.phase_2_test()
m_inst.match_status()
export(m_inst.matched)





