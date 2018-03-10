#custom sel_session
from Sel_session import *
class cSel_session(Sel_session):
	def __init__(self, url='http://www.fsf.org/'):
		super.__init__(url)
	def goto(self, x, element_id):
		self.driver.get(x)
    def go_to_TO(self, x, **kwargs):
        self.driver.get(x)
        try:
            WebDriverWait(self.driver, 10).until(readyCall())
        except TypeError as TE:
            print("TYPE ERROR")
            return
        except:
            raise(CustomTimeoutException("Timed out"))




class readyCall:
    def __init__(self, data = ''):
        self.data = data
    def __call__(self, driver):
        if driver.execute_script('document.getElementById("product_view") != null'):
            return True
        else:
            return False