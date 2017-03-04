#codes open
import codecs, csv

def r_csv_2(x,mode='rt', encoding = 'utf-8'):
    l = []
    csv_in = codecs.open(x, mode, encoding)
    myreader = csv.reader(csv_in)
    for row in myreader:
        l.append(row)
    csv_in.close()
    return l