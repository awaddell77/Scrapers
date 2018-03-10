#stand-alone program for reading CSVs
import csv
class R_csv:
	def __init__(self, fname):
		self.fname = fname
		self.mode = 'rt'
		self.encoding = 'utf-8'
		self.delimiter = ','
		self.__headers = []
	def get_headers(self):
		return self.__headers
	def set_headers(self, x):
		if not isinstance(x, list):
			raise TypeError("Param must be list")
		else:
			self.__headers = x
	def read_in(self):
		#reads csv into a list of lists
		l = []
		csv_in = open(self.fname, self.mode, encoding = self.encoding)
		myreader = csv.reader(csv_in, delimiter = self.delimiter)
		for row in myreader:
			l.append(row)
		csv_in.close()
		return l
	def dictionarify(self):
		items = self.read_in()
		#if headers is not an empty list it is inserted into the first row
		if self.__headers:
			items.insert(0, self.__headers)
		crit = items[0]
		#if something is not showing up in the final file it's probably because its column does not have a header
		results = []
		for i in range(1, len(items)):
			d = dict.fromkeys(crit, 0)
			for i_2 in range(0, len(crit)):
				try:
					print(items[i])
					print(items[i][i_2])
				except UnicodeEncodeError as UE:
					print("Unicode Error")
				d[crit[i_2]] = items[i][i_2]
			results.append(d)
		return results
