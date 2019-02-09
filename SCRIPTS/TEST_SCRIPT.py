import subprocess, os

def mutate_string(s,p,c):
	l = list(s)
	l[p] = c
	l = ''.join(l)
	print l

def clear():
    os.system('clear')

mutate_string('abracadabra',5,'k')
raw_input("PRESS ENTER TO CONTINUE")
subprocess.call("./pyinbash.sh", shell=True)
