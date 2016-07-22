from soupclass6 import *

#saves part of site
#
def feedstart(x,tag1,tag2,tag3):#writes data to memory for later use
    site = S_base(x,tag1, tag2, tag3).soup_target()
    
    
def test(x):
    #makes a true copy and then changes something in it
    test = deepcopy(x)
    test.html.append('<a>LOL</a>')
    return test
    
    
def g_keymaker(x,default='Key_'):
    d = {}
    for i in range(0, len(x)):
        d[default + str(i)] = x[i]
    return d

        
def check(x):
    orig = x
    new = test(x)
    for i in orig:
        if i not in new:
            print('Something has changed.')
    return False        
    
