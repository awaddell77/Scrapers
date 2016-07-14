#mysql 

from soupclass8 import C_sort,r_csv


def import_data(x):
	info = C_sort(x)
	db_columns = info.row(0)
	return db_columns