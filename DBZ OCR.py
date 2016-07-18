#Pannini DBZ card image handling
#designed to convert image text to actual text

import requests, lxml
import unicodedata
from PIL import Image

class S_img(object):
    def __init__(self, flink, ext='', fname=0, s = '/'):
        self.flink = flink
        self.fname = fname
        self.ext = ext
        self.s = s
    def d_img(self,n):#downloads image, returns file name
        img = requests.get(self.flink)
        img_n = self.flink.split('/')
        f = open(self.fname + self.ext ,'wb')
        f.write(img.content)
        f.close()
        return img_n
    def cardprep(self, x, x1, y1, x2, y2,  mono=0):
        cardIm = Image.open(x)
        #cropcardIm = cardIm.crop((62,447,413,576))
        cropcardIm = cardIm.crop((x1,y1,x2,y2))
        width, height = cropcardIm.size
        cropcardIm = cropcardIm.resize((width + 600 , height + 200))
        if mono != 0:
            if mono == 1:
                cropcardIm = cropcardIm.convert('L')#converts to monochrome
            if mono == 2:
                cropcardIm = cropcardIm.convert('1')#greyscale
        cropcardIm.save('test.jpg')

class S_img_hd(object):#image handling
    def __init__(self, fname):
        self.fname = fname
    sets = [(76, 344, 400, 594), (53, 374, 425, 527), (75, 375, 413, 521)]
    def cardprep_b(self):
        l = []
        card_n = self.fname.split('_')[0]
        n_fname = self.fname.split('.')[0]
        ext = self.fname.split('.')[1]
        cardIm = Image.open(self.fname)
        for i in range(0, len(self.sets)):
            cropcardIm = cardIm.crop(self.sets[i])
            width, height = cropcardIm.size
            cropcardIm = cropcardIm.resize((width + 600 , height + 300))
            n_name = 'test'+str(i)+self.fname
            l.append(card_n)
            l.append(n_name)
            cropcardIm.save(n_name)
        return l
        #cropcardIm = cardIm.crop((x1,y1,x2,y2))

    def tess_reader(self,x, y):#is the file name, y is the output
        subprocess.call(['tesseract', x,y])
        t_file = S_IO(y+'.txt').text_flex()
        return t_file
        
class S_chef(S_base):#for parsing through data in bsObjects and result sets
    #def __init__(self):#only self for now
    pass

