#look busy function
import time
import random

def loading(time1):
	try:
		int(time1)
	except ValueError as VE:
		print("Argument must be int")

	seconds = int(time1) * 60
	while time.clock() <= seconds:
		print("Processing item #{0}".format(random.randint(100,10000)))
		time.sleep(.5)
		print("Parsing results")



