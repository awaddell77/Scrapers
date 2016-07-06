#directory manager 

import os

def dir_change(x):
	current = os.getcwd()
	if current == x:
		print("%s is already the Current Working Directory" % (x))
	else:
		os.chdir(x)
		print("Working Directory has been changed from %s to %s" % (current, x))
