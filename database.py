#mysql 
import re
from soupclass8 import C_sort,r_csv

def login(x):
	pass

def import_data(x):
	info = C_sort(x)
	db_columns = info.row(0)
	db_contents = info.contents[1:]


	return db_columns, db_contents

def table_create(x, table_name, location=''):
	#creates table of text columns usings the provided list as column headers
	new = [re.sub(' ', '_', x[i].strip(' ')) + " TEXT" for i in range(0, len(x))]
	contents = ', '.join(new)
	if location == '':
		return 'CREATE TABLE ' + table_name + ' (' + contents + ') ;'
	else:
		return 'CREATE TABLE ' + table_name +'.'+ location + ' (' + contents + ') ;'


def table_data_prep(x):
	#adds quotes to every item on a csv list
	for i in range(0, len(x)):
		for i_2 in range(0, len(x[i])):
			x[i][i_2] = '"' + x[i][i_2] + '"'
	return x 
def table_insert(x, table):
	results = []
	x = table_data_prep(x)

	for i in range(0, len(x)):
		values = '(' + ', '.join(x[i]) + ') ;'
		command = 'INSERT INTO %s VALUES %s' % (table, values)
		#print(command)
		results.append(command)
	return results













