import random
def pn_randomizer(number, ch_limit = 0, new_number = True):
	newNumber = ""
	for i in range(0, len(number)):
		ch = random.randint(64, 123)
		flip = random.randint(0, 10)
		if flip > 5 and ch not in [64, 123] and ch not in range(91, 97):
			newNumber += chr(ch)
		else:
			newNumber += str(number[i])
	if ch_limit >= 1:
		newNumber = ""
		print("TESTING")
		for i in range(0, ch_limit):
			ch = random.randint(64, 123)
			if flip > 2 and ch not in [64, 123] and ch not in range(91, 97):
				newNumber += chr(ch)
			elif flip > 2 and flip <= 5:
				newNumber += chr(random.randint(97, 123))
			else:
				newNumber += str(random.randint(1,9))
		if new_number:
			return newNumber
		else:
			return number + newNumber
	return newNumber