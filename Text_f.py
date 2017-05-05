#text object
import csv
class Text_f:
	def __init__(self, fname):
		self.fname = fname
		self.delimiter = ''
		self.contents = []
		self.sorted_contents = []
		self.headers = []

	def read_in(self):
		words = ''
		l = []
		with open(self.fname, 'r') as f:
			data = f.readlines()
			for line in data:
				words = line.split(self.delimiter)
				print(words)
				l.extend(words)
			print(l)
		self.contents = l
	def split_data(self, delim):
		results = []
		new = []

		for i in self.contents:
			
			if i == delim and new:
				results.append(new)
				new = []
			elif i != delim and delim not in i and i:
				new.append(i)
			elif delim in i and i != delim:
				new.append(i)
				results.append(new)
				new = []
		self.sorted_contents = results

		return results
	def export_csv(self, output = 'FCfile.csv' ):
		if headers:
			self.sorted_contents.insert(0, headers)
		w_csv(self.sorted_contents, output)



