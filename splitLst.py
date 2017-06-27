#function that splits a list in half 

def splitLst(lst):
	#splits a list in two parts
	mid = len(lst) // 2
	p1 = lst[:mid]
	p2 = lst[mid:]
	return [p1, p2]


