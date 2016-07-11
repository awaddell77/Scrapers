#soup front end console



def main(*args):
	is_on = 1
	exit = ['Exit', 'exit', 'Quit', 'quit', 'bye']
	empty = ['',' ']
	while is_on == 1:
		command = input("Input: ")
		if command in exit:
			print("Now exiting.")
			is_on = 0
		elif command in empty:
			print("No command found.")
		else:
			com_exec(command.strip(' '))

def com_exec(x):
	commands = x.split(' ')
	com_list = ['Insert list of commands here']
	com_help = ['Help', 'help', '?']
	if x in com_help:
		print(com_list)
	else:
		if commands[0] == 'CFVG':
			if commands[1] in com_help:
				print("[INSTRUCTIONS ON HOW TO USE CARDFIGHT VANGUARD SCRAPER GO HERE]")
			else:
				main2(commands[1]) 
				#runs the Cardfight Vanguard Scraper (text file containing target links is the argument)




