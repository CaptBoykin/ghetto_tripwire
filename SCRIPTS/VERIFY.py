################################################
#                                              #
#  Script is passed a DB file, which is then   #
#  used as the main DB to compare versues a    #
#  'temp' table that is created.               #
#                                              #
################################################
 
from blessings import Terminal
import hashlib,  os, sys, getopt, platform, sqlite3, subprocess


db_banner = """
======================================================
CURRENT DATABASE FILE
======================================================
"""

#### USED BY THE pyinbash.sh SCRIPT TO PASS WHICH DB FILE TO USE ###
#__________________________________________________________________#

try:
    opts, args = getopt.getopt(sys.argv[1:],"dh",["db=","help"])
except getopt.GetoptError as err:
    print(err)
    sys.exit(2)

#====> DB file variable is set
for o,a in opts:
    if o in ("-d","--db"):
        db = a
    elif o in ("-h","--help"):
        usage()
        sys.exit()
    else:
        assert False, "unhandled option"
#####################################################################



### GLOBAL VARIABLES ###
#______________________#
conn = sqlite3.connect(db)
cursor = conn.cursor()
dbs_path = os.path.dirname(os.path.abspath(__file__))
dbs_filename = db
dbs_file_full = os.path.join(dbs_path,dbs_filename)
table_name = ""
t = Terminal()
########################



### FUNCTIONS ###
#_______________#

def clear():
        os.system('clear')

#====> PRODUCES THE DIFFERENCES BETWEEN THE TWO TABLES
def compare_tables():
    comp_table = "SELECT "+table_name+".pwd,"+table_name+".hash,"+table_name+".entry_date,temp.pwd,temp.hash,temp.entry_date FROM "+table_name+" LEFT OUTER JOIN temp ON "+table_name+".pwd = temp.pwd;"
    cursor.execute(comp_table)
    row = cursor.fetchall()
    for entry in row:
        v0 = str(entry[0])
        v1 = str(entry[1])
        v2 = str(entry[2])
        v3 = str(entry[3])
        v4 = str(entry[4])
        v5 = str(entry[5])
        
        if v1 != v4:
#### Keeping this block here, but it's useless I can
#### read from the old file itself to compare
#### Otherwise it is comparing it against itself (new vs new)
#### and will output nothing
#            try:
#                fp1 = open(v0,'r')
#                fp2 = open(v3,'r')
#                print "\nFile :"+fp1.name+"\nand\nFile :"+fp2.name+"\nHave been opened successfully!"
#                raw_input("\n<< PRESS ENTER TO CONTINUE >>\n\n")
#
#                fp1_line = fp1.readline()
#                fp2_line = fp2.readline()
#                while fp1_line != '' or fp2_line != '':
#                     fp1_line = fp1_line.rstrip()
#                     fp2_line = fp2_line.rstrip()
#                     if fp1_line != fp2_line:
#                         print t.red("\n==========[ OUTPUT ] =======================")
#                         print t.red(" FILE1 / LINE:"+fp1_line)
#                         print t.red(" FILE2 / LINE:"+fp2_line)
#                         print t.red(" ===================================================\n")
#                     fp1_line = fp1.readline()
#                     fp2_line = fp2.readline()
#                fp1.close()
#                fp2.close()
#
#            except IOError:
#                print "Could not open file!"

            print t.red("\n==========[ ERROR IN HASH ] =======================")
            print t.red(" FILE1: "+v0)
            print t.red(" HASH1: "+v1)
            print t.red(" DATE1: "+v2)
            print ("===================================================")
            print t.red(" FILE2: "+v3)
            print t.red(" HASH2: "+v4)
            print t.red(" DATE2: "+v5)
            print t.red(" ===================================================\n")
            

    raw_input("\n<< PRESS ENTER TO CONTINUE >>\n\n")

#====> HASHING THE DIRECTORY AND UPLOADING IT INTO A TEMP TABLE
def hash_temp(base,table_name):
    temp_table = """CREATE TABLE temp (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    pwd VARCHAR(255) NOT NULL,
                    hash VARCHAR(255) NOT NULL,
                    entry_date DATETIME DEFAULT CURRENT_TIMESTAMP);"""
    cursor.execute(temp_table)
    if os.path.isfile(dbs_file_full):
        for root,directory,files in os.walk(base,True):
            for local_file in files:
                input_file = root+"/"+local_file
                out = hashlib.sha256()
                out.update(open(input_file).read())
                out_hash = out.hexdigest()
                cursor.execute("INSERT INTO temp (pwd, hash) VALUES ('"+input_file+"','"+out_hash+"')")



#====> MAIN
def main():
    global table_name
    global dbs_file_full
    global dbs_filename
    global db_banner
    clear()
    print t.green(db_banner+dbs_file_full)

#====> LIST ALL TABLES THAT THE USER CAN SELECT
    cursor.execute("SELECT name FROM sqlite_master WHERE type = 'table';")
    query = cursor.fetchall()
    print "\nCURRENT TABLES:"
    for row in query:
        for entry in row:
            print entry
    table_name = raw_input("\n\nSELECT A TABLE\n\n\t$> ")
    tb_exists = "SELECT COUNT(*) FROM sqlite_master WHERE TYPE='table' AND NAME='"+table_name+"';"
#====> CHECK IF TABLE EXISTS
    cursor.execute(tb_exists)
    for row in cursor:
        if row[0] == 0:
            clear()
            raw_input("\n\nTABLE "+table_name+" DOES NOT EXIST!\nTRY AGAIN!")
            main()

#====> BEGIN INPUTS FOR THE TEMP TABLE SCAN
    base = raw_input("\n\nPLEASE SELECT A DIRECTORY PATH TO SCAN\n\nExample: /var/www/\n\n\t$> ")
    if os.path.isdir(base):
        if os.path.isfile(dbs_file_full):
            hash_temp(base,table_name)
            clear()
            raw_input("\n\n<< PRESS ENTER TO CONTINUE >>\n")
            compare_tables()
            cursor.execute("DROP TABLE temp;")
        else:
            clear()
            print "\n\n\nERROR! TRY AGAIN"
            main()

main()
conn.commit()
conn.close()
subprocess.call('./pyinbash.sh',shell=True)
