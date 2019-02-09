from blessings import Terminal
import getopt, sqlite3, os, subprocess, sys

t = Terminal()

def clear():
        os.system('clear')
try:
    opts, args = getopt.getopt(sys.argv[1:],"dh:t",["db=","help","table="])
except getopt.GetoptError as err:
    print(err)
    sys.exit(2)

for o, a in opts:
    if o in ("-d","--db"):
        db = a
        conn = sqlite3.connect(db)
        cursor = conn.cursor()
        if o in ("-t","--table"):
            table = a
            cursor.execute("SELECT * FROM "+table+";")
        else:
            clear()
            warning = t.bold_yellow('NO TABLE SPECIFIED.\nDEFAULTING TO default_hashes\n\nPRESS ENTER TO CONTINUE')
            raw_input(warning)
            cursor.execute("SELECT * FROM default_hashes;")
    elif o in ("-h","--help"):
        usage()
        sys.exit()
    else:
        assert False, "unhandled option"

row = cursor.fetchall()
for entry in row:
    v0 = str(entry[0])
    v1 = str(entry[1])
    v2 = str(entry[2])
    v3 = str(entry[3])
    
    print "\n======================================="
    print "ID   :"+v0
    print "NAME :"+v1
    print "HASH :"+v2
    print "DATE :"+v3
    print "=======================================\n"

raw_input("\n<< PRESS ENTER TO CONTINUE >>\n\n")
subprocess.call('./pyinbash.sh',shell=True)    
