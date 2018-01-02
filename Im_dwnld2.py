#Im_dwnld2
#for downloading items with request session
from Im_dwnld import *

class Im_dwnld2(Im_dwnld):
    def __init__(self, directory = "C:\\Users\\Owner\\Scrapers\\TEST DIR\\"):
        super().__init__(directory)
        self.session = requests.session()
        self.header = {"User-Agent": "Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36"}
    def i_main(self, ext_file, mask=""):
        urls = ext_file
        self.d_create(self.directory)
        name = ''
        for i in range(0, len(urls)):
            print("Now Downloading %s (Item #%d of %d)" % (urls[i], i+1, len(urls)))
            if not mask:
                name = self.d_img(urls[i])
            else:
                name = self.d_img(urls[i], mask)
        print('Downloaded %d files to %s' % (len(urls),self.directory))
        return name


    def import_cookies(self, cookies):
        #imports cookies from selenium session
        #header = {"User-Agent": "Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36"}

        self.session.headers.update(self.header)
        for i in cookies:
            c_d = {i['name']:i['value']}
            self.session.cookies.update(c_d)

    def d_img(self, x, mask= 0):#downloads image, returns file name
        ren = False
        try:
            img = self.session.get(x)
        except:
            print("Second attempt at %s" % x)
            img = self.session.get(x)
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
