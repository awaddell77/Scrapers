#comic formatting
import sys
def zero_lead(x, length=6):
	while len(str(x)) != length:
		x = '0' + str(x)
	return x
def comic_image_format(x):
	num = int(x)
	for i in range(1, num, 20000):
		if i + 20000 >= num:
			print("Found interval: It is {0} - {1}".format(i, i+19999))
			return i, i+20000

if __name__ == "__main__":
	comic_image_format(sys.argv[1])
