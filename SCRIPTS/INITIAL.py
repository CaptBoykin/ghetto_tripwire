################################################
#                                              #
#  Script creates and inserts values into DB   #
#                                              #
################################################


from blessings import Terminal
import hashlib,  os, sys, getopt, platform, sqlite3, subprocess

db_banner = """
======================================================
CURRENT DATABASE FILE
======================================================
"""

try:
    opts, args = getopt.getopt(sys.argv[1:],"dh",["db=","help"])
except getopt.GetoptError as err:
    print(err)
    sys.exit(2)

for o, a in opts:
    if o in ("-d","--db"):
        db = a
    elif o in ("-h","--help"):
        usage()
        sys.exit()
    else:
        assert False, "unhandled option"

conn = sqlite3.connect(db)
cursor = conn.cursor()
t = Terminal()
dbs_path = os.path.dirname(os.path.abspath(__file__))
dbs_filename = db
dbs_file_full = os.path.join(dbs_path,dbs_filename)

def clear():
        os.system('clear')

def hash_initial(base,table_name):
    if os.path.isfile(dbs_file_full):
        for root,directory,files in os.walk(base,True):
            for local_file in files:
                input_file = root+"/"+local_file
                out = hashlib.sha256()
                out.update(open(input_file).read())
                out_hash = out.hexdigest()
                cursor.execute("INSERT INTO "+table_name+" (pwd, hash) VALUES ('"+input_file+"','"+out_hash+"')")
                print input_file+":"+out_hash+"\n"
    

def main():
    global dbs_file_full
    global db_banner
    clear()
    print t.green(db_banner+dbs_file_full)
    cursor.execute("SELECT name FROM sqlite_master WHERE type = 'table';")
    query = cursor.fetchall()
    print "\nCURRENT TABLES:"
    for row in query:
        for entry in row:
            print entry
    table = raw_input("\n\nCREATE A NEW TABLE? (Y/N)\n\n\t$> ")
    table = table.upper()
    if table == "Y":
        clear()
        table_name = raw_input("\n\nPLEASE ENTER A NEW TABLE NAME\n\n\t$> ")
        table_name = str(table_name)
        query = "CREATE TABLE "+table_name+" ( id INTEGER PRIMARY KEY AUTOINCREMENT, pwd VARCHAR(255) NOT NULL, hash VARCHAR(255) NOT NULL, entry_date DATETIME DEFAULT CURRENT_TIMESTAMP);"
        cursor.execute(query)
        conn.commit()
    else:
        table_name = 'default_hashes'

    base = raw_input("\n\nPLEASE SELECT A DIRECTORY PATH TO SCAN\n\nExample: /var/www/\n\n\t$> ")
    if os.path.isdir(base):
        if os.path.isfile(dbs_file_full):
            hash_initial(base,table_name)    
            raw_input("\n\n<< PRESS ENTER TO CONTINUE >>\n")
            clear()
            print "\n\n\nHASHES FROM "+base+" HAVE BEEN UPLOADED TO "+dbs_file_full
            raw_input("\n\n<< PRESS ENTER TO CONTINUE >>\n")
        else:
            clear()
            print "\n\n\nERROR! TRY AGAIN"
            main()

main()
conn.commit()
conn.close()
subprocess.call('./pyinbash.sh',shell=True)
