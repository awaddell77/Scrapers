
class testclass(object):
	def __init__(self):
		self.value = 1
	def v_plus_one(self):
		return self.value + 1

class testclass1(object):
	def __init__(self):
		self._value = 1
	@property
	def value(self):
		return self._value
	
	@value.setter
	def value(self, x):
		self._value = x
	def v_plus_one(self):
		return self._value + 1
print(testclass().v_plus_one())
#print(testclass1().v_plus_one)
h = testclass1()

