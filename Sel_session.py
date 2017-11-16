from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup as bs
import lxml
import time

class Sel_session(object):
    def __init__(self, url='http://www.fsf.org/', *args):
        self.url = url
        self.args = args
        self.driver = webdriver.Firefox()
        #if true timeout enables the load_cutoff method in go_to
        self.timeout = False


    def start(self):
        self.driver.get(self.url)
        return self.driver
    def go_to(self,x, **kwargs):
        self.driver.get(x)
        if self.timeout:
            self.load_cutoff(kwargs.get("timeout", 10))
    def js(self, x):
        return self.driver.execute_script(x)
    def close(self):
        return self.driver.quit()
    def is_enabled(self, prod_id):
        #checks to see if the element is DISABLED
        result = self.js("return 'disabled' in document.getElementById(\'{0}\').attributes".format(prod_id))
        if result:
            #if disabled is listed among the element's attributes returns False
            return False
        else:
            return True
    def w_load(self, T_O = 30):
        #waits for page to finish loading
        count = 0
        while True:
            if self.driver.execute_script('return document.readyState') != "complete" and count <= T_O:
                count += 1
                time.sleep(1)
            elif count > T_O:
                break #should probably do something else

            else:
                break
    def load_cutoff(self, timeout = 10):
        
        start = time.time()
        while (time.time() - start) <= timeout and self.driver.execute_script('return document.readyState') != "complete":
            pass
        if (time.time() - start) > timeout:
            raise CustomTimeoutException("Timed out")





    def source(self):
        return bs(self.driver.page_source,'lxml')

    def element_check(self, element):
        try:
            self.driver.find_element_by_id(element)
        except:
            return False
        else:
            return True

class CustomTimeoutException(Exception):
    '''Raised whenever browser exceeds a time out variable while loading a page'''
