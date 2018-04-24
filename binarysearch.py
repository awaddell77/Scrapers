#binary search for list
import time
def bsearch(lst, val):
	low = 0
	r = len(lst)-1
	for i in lst:
		if low > r: return -1
		mid = (r + low)//2
		if lst[mid] < val: low = mid + 1
		elif lst[mid] > val: r = mid - 1
		else: return mid
def linsearch(lst, val):
	for i in lst:
		if i == val: return val
	return -1
testlst = [i for i in range(0, 10001)]

def test():
	s1 = time.time()
	linsearch(testlst, 6500000)
	print("Linear Search took {0} seconds".format(time.time() - s1))
	s2 = time.time()
	bsearch(testlst, 6500000)
	print("Binary Search took {0} seconds".format(time.time() - s2))




