#alpha sort

def alpha_sum(x):
	sum_of_str = 0
	for i in x:
		n = ord(i)
		if ord(i) < 97 and 91 > ord(i) > 64:
			n = ord(i) + 32
		sum_of_str += n
	return sum_of_str

print(alpha_sum("Apples") < alpha_sum("Zebras"))




