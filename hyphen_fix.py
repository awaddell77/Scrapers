#removes commonly used unicode hypens and replaces them with ascii hyphens

def hyphix(x):
	#takes string
	hyph_lst = ['\u2013', '\u1806','\u2010', '\u2011', '\u2012', '\u2014']
	for i in hyph_lst:
		x = x.replace(i, '-')
	return x
