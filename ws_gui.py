from tkinter import *
from tkinter.filedialog import *
from date_form import *
from text_l import *
from dbaseObject import *
import getpass
from dictionarify import *
from ws_scrape import *

class Dbase_gui:
	def __init__(self):
		#self.__username = input("Enter username: ")
		#self.__password = getpass.getpass('Enter password: ')
		self.m_inst = Ws_scrape()
		window = Tk()
		self.lbl = Label(window, text='Enter link')
		self.lbl2 = Label(window, text="Submit data")
		self.ent_field = Text(window, height = 1, width = 10)
		#function name only, no parentheses at the end
		self.btsub = Button(window, text="Click to start scraping process", command = self.get_text)
		self.ent_field.pack()
		self.lbl.pack()
		self.btsub.pack()
		self.lbl2.pack()
		self.fname = ''
		self.dir_n = ''
		self.lst = []
		#self.creds = text_l('C:\\Users\\Owner\\Documents\\Important\\catcred.txt')
		window.mainloop()
	def get_text(self):
		StringVar = self.ent_field.get('1.0', 'end')
		StringVar = re.sub('\n', '', StringVar)
		print(StringVar)
		self.m_inst.set_start(StringVar)
	def get_lst(self):
		return self.lst
	def get_file(self, master = True):
		fname1 = askopenfilename()
		#if '.csv' not in fname1.split('/')[len(fname1.split('/'))-1]:
			#raise TypeError("Can only import CSV files")
		if master:
			self.m_inst.master = fname1
		else:
			self.m_inst.preview = fname1
	def set_dir(self):
		new_dir = askdirectory()
		self.dir_n = new_dir
		print("Directory is now", new_dir)
	def sub_id(self):
		pass



#test_inst = Scraper_gui()
if __name__ == "__main__":
	test_inst = Dbase_gui()
