#class testing

class Shape:
	def __init__(self, name, weight):
		self.name = name
		self.weight = weight
	def print_weight(self):
		print(self.weight)
	def add_5(self, x):
		return x + 5

class Triangle(Shape):
	def __init__(self, angles)
