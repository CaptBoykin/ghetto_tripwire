import sqlite3, os, sys, subprocess, getopt

def clear():
        os.system('clear')

new_table = """
CREATE TABLE default_hashes (
id INTEGER PRIMARY KEY AUTOINCREMENT,
pwd VARCHAR(255) NOT NULL,
hash VARCHAR(255) NOT NULL,
entry_date DATETIME DEFAULT CURRENT_TIMESTAMP);
"""
tb_exists = """
SELECT COUNT(*) FROM sqlite_master
WHERE TYPE='table' AND NAME='default_hashes'
"""

def usage():
    print """
+=========================================+
| Usage:                                  |
|                                         |
|  python CREATE_DEFAULT.py --db mydb.db  |
|                                         |
|  python CREATE_DEFAULT.py --help        |
|                                         |
+=========================================+
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
#new_table = "CREATE TABLE "+table_name+" ( id INTEGER PRIMARY KEY AUTOINCREMENT, pwd VARCHAR(255) NOT NULL, hash VARCHAR(255) NOT NULL, entry_date DATETIME DEFAULT CURRENT_TIMESTAMP);"
#tb_exists = "SELECT COUNT(*) FROM sqlite_master WHERE TYPE='table' AND NAME='"+table_name+"';"


cursor.execute(tb_exists)
for row in cursor:
    if row[0] == 0:
        cursor.execute(new_table)
        conn.commit()
        cursor.execute(tb_exists)
        for row in cursor:
            if row[0] > 0:
                clear()
                raw_input("\n\nTABLE 'default_hashes' HAS BEEN SUCCESSFULLY CREATED!\nPRESS ENTER TO CONTINUE")
    else:
        clear()
        raw_input("\n\nTABLE 'default_hashes' ALREADY EXISTS\nPRESS ENTER TO CONTINUE")
    
conn.close()
subprocess.call('./pyinbash.sh',shell=True)
