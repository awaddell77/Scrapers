#command line test
import sys



def test_f(x):
	for i in x[1:]:
		print(i)
		print(type(i))

def test_int(x):
	for i in x[2:]:
		try:
			int(i)
			print(i)
		except ValueError as VE:
			print("%s is not a number" % i)
		else:
			print("%d is a number" % int(i))
if sys.argv[1] == 'f':
	test_f(sys.argv)
elif sys.argv[1] == 'int':
	test_int(sys.argv)
#test_f(sys.argv)

