from w_csv import *
from S_format import *
#as the name of the funciton suggests, this will write data from a list of a dicts to a csv 
def export_dictionarify(data, c= [], fname = 'report_file.csv' ):
	if c: crit = c
	else: crit = list(data[0].keys())
	res = [crit]
	for i in data:
		res.append(S_format(i).d_sort(crit))
	w_csv(res, fname)
	return
