







class I_dwnld(object):#not tested and probably does not work
    def __init__(self, directory ='BATCH DOWNLOAD'):
        self.directory = directory

    def main(self, ext_file = 0):
    	urls = ext_file
        self.d_create(self.directory)
        for i in range(0, len(urls)):
            print("Now Downloading %s (Item #%d of %d)" % (urls[i], i+1, len(urls)))
            self.d_img(urls[i],self.directory)
        return 'Downloaded %d files to %s' % (len(urls),self.directory)

    def main2(self, n = 0,  link=1):
        file = C_sort(self.fname)
        urls = file.column(link)
        names = file.column(n)
        self.d_create(self.directory)
        for i in range(0, len(urls)):
            print("Now Downloading %s (Item #%d of %d)" % (urls[i], i+1, len(urls)))
            self.d_img(urls[i],names[i], self.directory)
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
        if '.' not in fname:
            print('This file has no extension')
            return fname,''
        else:
            lfname = fname.split('.')
            ext = lfname[len(lfname)-1]
            return fname, ext
            
    def d_img(self, x, mask= 0,d_dir='C:\\Users\\Owner\\'):#downloads image, returns file name
        img = requests.get(x)
        img_n = self.n_exts(x)
        if mask != 0:
            img_n = [mask + '.' + img_n[1]] #has to be list for consistency
        f = open(join(d_dir, img_n[0]) ,'wb')
        f.write(img.content)
        f.close()
        return img_n
