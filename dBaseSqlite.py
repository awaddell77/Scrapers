#sqlite3
import sqlite3

class dBaseSqlite:
    def __init__(self, databaseFile):
        self.databaseFile = databaseFile
        if not isinstance(self.databaseFile, str): raise TypeError("Must be str")
        self.con = sqlite3.connect(self.databaseFile)
        self.cursor = self.con.cursor()
        self.last_resp = ''
    def query(self, x):
        #returns a 2d list object containing tuples
        #e.g. [(1, 'ITEM #1'), (2, 'ITEM #2'), (3, 'ITEM #3')]
        self.cursor.execute(x)
        rows = self.cursor.fetchall()
        self.last_resp = rows
        return rows
	def command(self, x):
		self.cursor.execute(x)
		self.con.commit()


#for testing only
test = dBaseSqlite('C:\\Users\\Owner\\testDB.db')
try:
    test2 = dBaseSqlite(test)
except TypeError as TE:
    print("Raised the TypeError")
res = test.query('SELECT * from testTable;')
print(res)
