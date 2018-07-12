from w_csv import *
from dictionarify import *
from S_format import *
from cleaner import *

def clean(fname, tbr):
	data = dictionarify(fname)
	keys = list(data[0].keys())
	for custs in data:
		custs["Keller_Name"] = custs["Name"]
		for i in tbr:

			if i == '/ ' in custs["Name"]: custs["Name"] = custs["Name"].replace(i, ' ').strip(' ')
			elif i in custs["Name"]: custs["Name"] = custs["Name"].replace(i, '').strip(' ')
	return data
def dc(fname):
	#just got tired of writing dictionarify over and over again in the shell
	return dictionarify(fname)

def transform_by_phone(datafile):
	phone_d = {}
	for custs in datafile:
		if custs["PHONE_1"] and not phone_d.get(custs["PHONE_1"], ''): phone_d[custs["PHONE_1"]] = cust

def trans_by_co(datafile):
	for ags in datafile:
		if ', ' in ags["Name"] and 'CITY OF - ' not in ags["Name"]:
			n_lst = ags["Name"].split(', ')
			print("Old name: {0}".format(ags["Name"]))
			n_name = n_lst[1].strip(' ') + ' ' + n_lst[0].strip(" ")
			print("New name: {0}".format(n_name))
			ags["Name"] = n_name
		elif ', ' in ags["Name"] and 'CITY OF - ' in ags["Name"] and 'HOUSING AUTHORITY' not in ags["Name"]:
			n_lst1 = ags["Name"].split(' - ')
			n_lst = n_lst1[0].split(', ')
			print("Old name1: {0}".format(ags["Name"]))
			n_name = n_lst[1].strip(' ') + ' ' + n_lst[0].strip(" ") + ' - ' + n_lst1[1]
			print("New name: {0}".format(n_name))
			ags["Name"] = n_name
		elif ', ' in ags["Name"] and 'CITY OF - ' in ags["Name"] and 'HOUSING AUTHORITY' in ags["Name"]:
			n_lst1 = ags["Name"].split(' - ')
			n_lst = n_lst1[0].split(', ')
			n_name = n_lst[0].strip(' ') + ' HOUSING AUTHORITY'
			ags["Name"] = n_name


	#w_csv(datafile, "transformed.csv")
	return datafile

def name_hash(datafile):
	for i in datafile:
		#i["Name"]
		pass

def reductive_search(datafile):

	res_data = {}
	for custs in datafile:
		name = custs["Name"].split(' ')
		for i in name:
			pass
		pass
def phase_1(new_d, master_data):
	matched = []
	for i in range(len(new_d)-1, -1, -1):
		new_d[i]["Cust_id"] = ''
		new_d[i]["Matched_w"] = ''
		#ags["Matched"] = False
		new_d[i]["Keller_Name"] = ''
		for i_2 in range(len(master_data)-1, -1, -1):
			if new_d[i]["Name"].lower() == master_data[i_2]["Name"].lower():
				#ags["Matched"] = True
				#print("Found match for {0}".format(new_d[i]["Name"]))
				new_d[i]["Keller_Name"] = master_data[i_2]["Keller_Name"]
				new_d[i]["Cust_id"] = master_data[i_2]["Customer"]
				new_d[i]["Matched_w"] = master_data[i_2]["Name"]

				matched.append(new_d.pop(i))
				matched[len(matched)-1]['Phase'] = 1
				del master_data[i_2]
				break
	return matched
def clean_test(fname, tbr):
	res = clean(fname, tbr)
	results = []
	for i in res:
		results.append(S_format(i).d_sort(1))
	#w_csv(results, "cleantest.csv")
	return res

def export(datafile, fname = 'matchfile.csv'):
	crits = list(datafile[0].keys())
	results = [crits]
	for i in datafile:
		results.append(S_format(i).d_sort(crits))
	w_csv(results, fname)

def phase_1_test(state_clients, master):

	new_d = trans_by_co(dc(state_clients))
	master_d = clean(master, ['#', '*', '$'])
	res = phase_1(new_d, master_d)
	#export(res)
	return res
def word_match(ag_name, client_name, ignore = ['the'], thresh = .99):
	#ag_name = ag_name.replace('the', '')
	#client_name = client_name.replace('the', '')
	ag_name = cleaner(ag_name.lower(), ignore)
	client_name = cleaner(client_name.lower(), ignore)
	#print(ag_name, client_name)
	ag_lst = ag_name.lower().split(' ')
	#print("ag_list: ", ag_lst)
	client_name = client_name.lower()
	match = 0
	for word in ag_lst:
		if word != "the" and word in client_name:
			#print("{0} is in {1}".format(word, client_name))
			match += 1
	if match / len(ag_lst) >= thresh: return True
	return False
def phase_2(new_d, master_data):
	matched = []
	
	for i in range(len(new_d)-1, -1, -1):
		new_d[i]["Cust_id"] = ''
		new_d[i]["Matched_w"] = ''
		#ags["Matched"] = False
		for i_2 in range(len(master_data)-1, -1, -1):
			if word_match(new_d[i]["Name"].lower(), master_data[i_2]["Name"].lower(), ignore = ['the'], thresh = .95):
				#ags["Matched"] = True
				#print("Found match for {0}".format(new_d[i]["Name"]))
				new_d[i]["Cust_id"] = master_data[i_2]["Customer"]
				new_d[i]["Matched_w"] = master_data[i_2]["Name"]
				new_d[i]["Keller_Name"] = master_data[i_2]["Keller_Name"]
				
				matched.append(new_d.pop(i))
				del master_data[i_2]
				break
	return matched