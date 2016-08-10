
from soupclass8 import text_lc,w_csv
import sys



class Csv_gen(object):
    def __init__(self, fname):
        self.fname = fname
    def main1(self,n):#for text files with multiple lines for each item
        h = text_lc(self.fname)
        j = self.list_t(h)
        l = self.row_m(h,n)
        w_csv(l)
        return l

    def main2(self): #for text files where each item occupies a single line
        m = text_lc(self.fname)
        h = self.list_t(m)
        f = self.row_s(h)
        w_csv(f)
        return f        
    def text_l(self):
        words = ''
        n = 0
        row1 = []
        row2 = []
        with open(self.fname, 'r') as f:
            data = f.readlines()
            for line in data:
                    words = line.split('\n')
                    if words != '' or words != ' ' :
                        l.append(words)
                        #print "WORKED!"
        print(l)
        return l
    def list_t(self, x): #takes lists, sorts through and removes ''
        h = []
        for i in range(0, len(x)):
            for contents in x[i]:
                if contents != '':
                    h.append(contents)
        print(h)
        return h
    def row_m(self, x,n):#n is the number of lines each element should contain
        a = []
        b = []
        for i in range(0,len(x)):
            #n = n + 1
            a.append(x[i])
            if len(a) == n:
                b.append(a)
                a = []
            print(x[i])
        return b

    def row_s(self, x):
        a = []
        b = []
        n = 0
        for i in range(0,len(x)):
            #n = n + 1
            a.append(x[i])
            if len(a) == 1:
                b.append(a)
                a = []
            print(x[i])
        return b

if '-m' in sys.argv:
    Csv_gen(sys.argv[1]).main1(sys.argv[3])
    print("Finished")
elif '-s' in sys.argv:
    Csv_gen(sys.argv[1]).main2()
    print("Finished")
else:
    print("[file name] [-m/-s] [# of lines]")