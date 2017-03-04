#duplicate finder
from soupclass8 import *

def dupe_find_d(d_list, x, crit="Product Name"):
	#sorts through list of dictionaries and tries to match the value (x) with the key (crit) of any dictionary element in the list
	results = []
	crit_list = ["Product Name", "Product Id"]
	for i in range(0, len(d_list)):
		if d_list[i][crit] == x:
			res = S_format(d_list[i]).d_sort(crit_list)
			res.append(i)
			results.append(res)
	return results




def standardize_text(x):
	x = x.strip(' ')
	x = re.sub('-', ' ', x)
	
