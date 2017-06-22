

#testing  overloading

class t1(object):
	def __init__(self, name):
		self.name = name
	def p_data(self):
		print(self.name)
	def name_plus(self, x):
		print(self.name + x)

class t2(t1):
	def __init__(self, data):
		super().__init__("child")
		self.data = data
		self.name_plus(" works in the init")
	def p_data(self, x):
		print(self.data + x)

test = t2('testing')
test.p_data(" this")
test.name_plus(" is working")
