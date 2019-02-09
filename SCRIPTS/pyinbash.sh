#!/bin/bash


####### ======  Bye Felicia! ===== #########
goodbye()
{
echo "


***************************
*                         *                      
*       kthnxbye          *
*                         *
***************************

"
}
###########################################



####### ======  Exit confirm menu ===== #########
exit_confirm()
{
    dialog --title "Ghetto Tripwire" \
           --backtitle "Created by Tyler Boykin"\
           --yesno "Are you sure you want to quit?" 7 30

    local response=$?
    case $response in
        0               ) clear && goodbye;;
        1               ) clear && sh ./pyinbash.sh;;
        255             ) clear && sh ./pyinbash.sh;;
        ${DIALOG_ESC}   ) sh ./pyinbash.sh;;
        ${DIALOG_CANCEL}) sh ./pyinbash.sh;;
    esac
}
###########################################


####### ======  Create a DB ===== #########

quick_check()
{
    if [ -e "$file_name" ]
    then
        clear
        echo
        echo "$file_name ALREADY EXISTS!"
        echo "PRESS ENTER TO CONTINUE"
        read
        sh ./pyinbash.sh
    else
        `touch "$file_name"`
        clear
        echo
        echo "$file_name WAS CREATED SUCCESSFULLY!"
        echo "PRESS ENTER TO CONTINUE"
        read
        sh ./pyinbash.sh
    fi
}

create_d()
{
    dialog --title "Create Database File"\
           --backtitle "Created by Tyler Boykin"\
           --inputbox "Please Enter a Database Name\nExample: MY_DB.db\nExample: /my/dir/MY_DB.db" 10 60 2>TEMP/tempc

    file_name=`cat TEMP/tempc`

    local response=$?
    case $response in
        0               ) clear && quick_check;;
        1               ) clear && sh ./pyinbash.sh;;
        255             ) clear && sh ./pyinbash.sh;;
        ${DIALOG_ESC}   ) sh ./pyinbash.sh;;
        ${DIALOG_CANCEL}) sh ./pyinbash.sh;;
    esac
}
###########################################


####### ======  Create a table ===== #########
create_t()
{
    dialog --title "Create a Default Table"\
           --backtitle "Created by Tyler Boykin"\
           --inputbox "Please Specify Your Database File\nExample: DB.db\nExample: /my/dir/MY_DB.db" 10 60 2>TEMP/tempa

    local file_name=`cat TEMP/tempa`

    local response=$?
    case $response in
        1               ) clear && sh ./pyinbash.sh;;
        0               ) python 'CREATE_TABLE.py' --db $file_name;;
        255             ) clear && sh ./pyinbash.sh;;
        ${DIALOG_ESC}   ) sh ./pyinbash.sh;;
        ${DIALOG_CANCEL}) sh ./pyinbash.sh;;
    esac

   # python 'CREATE_TABLE.py' --db $file_name
}
###########################################


####### ======  Read Table ===== ##########
#### ====== Two nested functions ===== ####
#
#
#pick_table()
#{
#    dialog --title "Create a Default Table"\
#           --backtitle "Created by Tyler Boykin"\
#           --inputbox "Please Specify Your Database Name"10 60 2>TEMP/tempe
#    local DB=`cat TEMP/tempe`
#    local response=$?
#    case $response in
#        1               ) clear && sh ./pyinbash.sh;;
#        0               ) python 'READ_TABLE.py' --db "$FILE" --table "$DB";;
#        255             ) clear && sh ./pyinbash.sh;;
#      ${DIALOG_ESC}   ) sh ./pyinbash.sh;;
#        ${DIALOG_CANCEL}) sh ./pyinbash.sh;;
#    esac
#}

pick_db()
{
    DIR=$PWD
    FILE=$(dialog --title "Read Table Entries"\
                  --backtitle "Created by Tyler Boykin"\
                  --stdout --title "Please Specify a DB"\
                  --fselect "$DIR"/  14 48)

    local response=$?
    case $response in
        1               ) clear && sh ./pyinbash.sh;;
        0               ) python 'READ_TABLE.py' --db "$FILE";;
        255             ) clear && sh ./pyinbash.sh;;
        ${DIALOG_ESC}   ) sh ./pyinbash.sh;;
        ${DIALOG_CANCEL}) sh ./pyinbash.sh;;
#       *               ) clear && pick_table;;
    esac

}
###########################################


####### ======  Initial Hasing  ===== #########
initial()
{
    dialog --title "Modify Tables and Upload Hashes"\
           --backtitle "Created by Tyler Boykin"\
           --inputbox "Please Specify Your Database File\nExample: MY_DB.db\nExample: /my/dir/MY_DB.db" 10 60 2>TEMP/tempd

    local file_name=`cat TEMP/tempd`

    local response=$?
    case $response in
        1               ) clear && sh ./pyinbash.sh;;
        0               ) python 'INITIAL.py' --db $file_name;;
        255             ) clear && sh ./pyinbash.sh;;
        ${DIALOG_ESC}   ) sh ./pyinbash.sh;;
        ${DIALOG_CANCEL}) sh ./pyinbash.sh;;
    esac

    #python 'INITIAL.py' --db $file_name
}
###########################################


####### ======  Verify Hasing  ===== #########
verify()
{

    DIR=$PWD
    FILE=$(dialog --title "Read Table Entries"\
                  --backtitle "Created by Tyler Boykin"\
                  --stdout --title "Please Specify a DB"\
                  --fselect "$DIR"/  14 48)

    local response=$?
    case $response in
        1               ) clear && sh ./pyinbash.sh;;
        0               ) python 'VERIFY.py' --db "$FILE";;
        255             ) clear && sh ./pyinbash.sh;;
        ${DIALOG_ESC}   ) sh ./pyinbash.sh;;
        ${DIALOG_CANCEL}) sh ./pyinbash.sh;;
#       *               ) clear && pick_table;;
    esac

}
###########################################

####### ======  Main menu ===== #########
menu()
{
    dialog --title "Ghetto Tripwire" \
           --backtitle "Created by Tyler Boykin"\
           --menu "Main Menu" 20 50 10 \
            Test "Execute External Test Script"\
            Create "Create a new DB File"\
            Default "Create a Default Table"\
            Initial "Perform Initial Hashing"\
            Verify "Hash Verification"\
            View "View A Table"\
            About "About && Readme" 2>TEMP/temp
}
###########################################



####### ======  (main) program  ===== #########

menu
input=`cat TEMP/temp`

case "$input" in
    "Test"          ) clear && python 'TEST_SCRIPT.py';;
    "Create"        ) clear && create_d;;
    "Default"       ) clear && create_t;;
    "Initial"       ) clear && initial;;
    "Verify"        ) clear && verify;;
    "View"          ) clear && pick_db;;
    "About"         ) clear && python 'README.py';;
    ${DIALOG_ESC}   ) clear && exit_confirm;;
    ${DIALOG_CANCEL}) sh ./pyinbash.sh;;
esac



