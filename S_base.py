from bs4 import BeautifulSoup as bs
import requests, lxml, os
class S_base(object):
    def __init__(self, url, **kwargs):
        self.url = url
        self.tag1 = kwargs.get('tag1',None)
        self.tag2 = kwargs.get('tag2',None)
        self.tag3 = kwargs.get('tag3',None)
    def soupmaker(self):#makes the soup
        html = requests.get(self.url)
        html = html.content
        bsObject = bs(html, 'lxml')
        return bsObject

        
    def soupmaker_catch(self, T_O = 1.500):#T_O is the amount of time in seconds requests will wait for a response
        try:
            html = requests.get(self.url, timeout= T_O)
        except:
            print("There probably was a ConnectionError for %s" % (self.url))
            return False
            

        else:
            html = html.content
            bsObject = bs(html, 'lxml')
            return bsObject
    def soupmaker_batch(self,limit=10): 
        #limit refers to the number of times the while loop will call the soupmaker_catch method
        n = 1
        site = self.soupmaker_catch()
        print('Attempting to process %s' % (self.url))
        while not site:
            print('Connection Failed. Retrying. This is attempt #%d' % (n))
            site = self.soupmaker_catch()
            n += 1
            if n == limit:
                return '%s could not be reached.' % (self.url)
        return site





    def soupmaker_bot(self):
        headers = {'User-Agent':'Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)'}
        html = requests.get(self.url, headers=headers)
        html = html.content
        bsObject = bs(html, 'lxml')
        return bsObject


    def stealth_smaker(self):
        headers = {'User-Agent': 'Mozilla/5.0 (iPad; U; CPU OS 3_2_1 like Mac OS X; en-us) AppleWebKit/531.21.10 (KHTML, like Gecko) Mobile/7B405'}
        html = requests.get(self.url, headers= headers)
        html = html.content
        bsObject = bs(html, 'lxml')
        return bsObject
    def sel_soup(self, quit = 0, wait= 0, scroll = 0):#uses Selenium to retrieve the site's html code, good for sites with lots of JS
        browser = webdriver.Firefox()
        #browser = webdriver.PhantomJS()
        #too many ifs, fix control flow
        browser.get(self.url)
        if scroll != 0:
            browser.execute_script("window.scrollTo(0,10)")
        if wait != 0:
            browser.implicitly_wait(wait)

        html = browser.page_source
        if quit == 0:
            browser.quit()
            bsObject = bs(html, 'lxml')
            return bsObject
        if quit != 0:
            bsObject = bs(html, 'lxml')
            return bsObject


    def soup_target(self):
        if self.tag2 == 0 or self.tag3 == 0:
            return self.soupmaker().find(self.tag1)#if tag2 or tag 3 are 0 then it only looks for the first tag
        else:
            return self.soupmaker().find(self.tag1,{self.tag2:self.tag3})
    def soup_tnet(self):
        return self.soupmaker().find_all(tag1)
    
    def link_s_t(self,n):#takes bsObject with isolated link table and scrapes links, n is the number of columns
        links = self.soup_target()
        links = links.find_all('a')#gets all links
        print(links)
        l = []
        n_l = []#for the full url
        bad_l = ['www.amazon.com', 'www.amazon.co.uk', '']
        for i in range(0, len(links), n):#there are 4 columns 
            link1 = S_format(str(links[i])).linkf('href=')
            if link1 not in bad_l and link1 not in l:
                l.append(S_format(str(links[i])).linkf('href='))
        return l

    def soupmaker_local(self, fname, directory=os.getcwd()):
        #for opening source code that is saved locally
        if os.name == 'nt': site = bs(open(directory + '\\' + fname, 'lxml'))
        else: site = bs(open(directory + '/' + fname, 'lxml'))

        #need to add directory selection in the future
        return site
