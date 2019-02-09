from blessings import Terminal
import hashlib,  os, sys, platform, sqlite3

dbs_path = os.path.dirname(os.path.abspath(__file__))
dbs_filename = "TEST_DB.db"
dbs_file_full = os.path.join(dbs_path,dbs_filename)
conn = sqlite3.connect("TEST_DB.db")
cursor = conn.cursor()

def clear():
        os.system('clear')


def hash_initial(base):
    for root,directory,files in os.walk(base,True):
        for local_file in files:
            input_file = root+"/"+local_file
            out = hashlib.sha256()
            out.update(input_file)
            out_hash = out.hexdigest()
            cursor.execute("INSERT INTO hash (pwd, hash) VALUES ('"+input_file+"','"+out_hash+"')")
            print input_file+":"+out_hash+"\n"


def main():
    global dbs_path
    global dbs_filename
    clear()
    base = raw_input("\n\nPLEASE SELECT A VALUE DIRECTORY PATH TO SCAN\n\nExample: /var/www/\n\n\t$> ")
    if os.path.isdir(base):
        hash_initial(base)






##### ===== DB Filler / Test Inserts ===== ######
"""
for i in range(0,10):
    for x in range(0,10):
        i = str(i)
        x = str(x)
        cursor.execute("INSERT INTO hash (pwd, hash) VALUES ('"+i+"','"+x+"')")
"""


main()
conn.commit()
conn.close()
