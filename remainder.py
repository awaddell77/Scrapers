#remainder

def rem(n, x):
    amount = n ** x
    count = 0
    rem = 0
    while True:
        if amount == 0:
            return count
        amount = amount // n
        count += 1
def remAlgo(n, n2):
    amount = n
    count = 0
    rem = 0
    while True:
        if amount >= n2:
            return count
        amount = amount * 2
        count += 1
