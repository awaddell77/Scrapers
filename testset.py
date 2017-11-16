import time

def test_prog():
	#start = time.time()
	testSet = {i for i in range(0, 100000000)}
	testLst = [i for i in range(0, 100000000)]
	n = 0
	start = time.time()
	for i in testSet:
		n = 1 * i
	setTime = time.time() - start
	start = time.time()
	n = 1
	for i in testLst:
		n = 1 * i
	lstTime = time.time() - start
	print("Set took {0} seconds to iterate through".format(setTime))
	print("List took {0} seconds to iterate through".format(lstTime))

if __name__ == "__main__":
	test_prog()


		


