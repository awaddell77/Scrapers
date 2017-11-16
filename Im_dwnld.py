import re, requests, os
from os.path import join
import imghdr


class Im_dwnld(object):
    def __init__(self, directory = "C:\\Users\\Owner\\Scrapers\\TEST DIR\\"):
        self.directory = directory

    def i_main(self, ext_file = 0):
        urls = ext_file
        self.d_create(self.directory)
        for i in range(0, len(urls)):
            print("Now Downloading %s (Item #%d of %d)" % (urls[i], i+1, len(urls)))
            self.d_img(urls[i])
        return 'Downloaded %d files to %s' % (len(urls),self.directory)

    def main2(self, n = 0,  link=1):
        file = C_sort(self.fname)
        urls = file.column(link)
        names = file.column(n)
        self.d_create(self.directory)
        for i in range(0, len(urls)):
            print("Now Downloading %s (Item #%d of %d)" % (urls[i], i+1, len(urls)))
            self.d_img(urls[i], self.directory, names[i])
        return 'Downloaded %d files to %s' % (len(urls),self.directory)




    def d_create(self,new_dir):
        new_dir = self.directory
        if '//' not in new_dir:
            new_dir = re.sub('/', '//', new_dir)
        if os.path.isdir(new_dir):
            print("Directory already exists")
            return False
        else:
            os.mkdir(new_dir)
            print("New Directory Created")
            return new_dir

    def ext_grab(self,x):
        new = x.split('.')
        return new[len(new)-1]

    def n_grab(self, x):
        new = x.split('/')
        return new[len(new)-1]


    def n_exts(self,x):
        #extracts the filename and its extension from a link
        if '/' not in x:
            return 'This is not a url'
        link = x.split('/')
        fname = link[len(link)-1]
        lfname = fname.split('.')

        if '.' not in fname:
            print('This file has no extension')
            return fname,''
        else:
            lfname = fname.split('.')
            ext = lfname[len(lfname)-1]
            return fname, ext

    def d_img(self, x, mask= 0):#downloads image, returns file name
        ren = False
        try:
            img = requests.get(x)
        except:
            print("Second attempt at %s" % x)
            img = requests.get(x)
        img_n = self.n_exts(x)
        if not img_n[1]:
            print("TESTED")
            ren = True
        if mask != 0:
            img_n = [mask + '.' + img_n[1]] #has to be list for consistency
        f = open(join(self.directory, img_n[0]) ,'wb')
        f.write(img.content)
        f.close()
        if ren:
            ext = imghdr.what(join(self.directory, img_n[0]))
            if ext is not None:
                nName = img_n[0] + ext
                try:
                    os.rename(join(self.directory, img_n[0]), join(self.directory, nName))
                except FileExistsError as FE:
                    #overwrites old images
                    os.remove(join(self.directory, nName))
                    os.rename(join(self.directory, img_n[0]), join(self.directory, nName))
                    return nName
                else:
                    return nName



        return img_n
