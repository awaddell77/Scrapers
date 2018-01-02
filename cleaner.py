import re
def cleaner(x, tbr):#x is the item, tbr is a list of sub-strings that need to be removed
    for i in range(0, len(tbr)):
        x = re.sub(tbr[i], '', x)
    return x
