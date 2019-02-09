#!/bin/bash
#Author = Tyler Boykin

# This script starts everything off


clear
cat "SCRIPTS/TRIPWIRE_BANNER.txt"
read
clear
echo "

    DO YOU WANT TO AUTO-INSTALL ALL NECESSARY PYTHON MODULES (USING PIP? 
         
                                Y OR N ??
"
read ANSWER

### integrate at some point ###
#case "$OSTYPE" in
#  solaris*) echo "SOLARIS" ;;
#  darwin*)  echo "OSX" ;; 
#  linux*)   echo "LINUX" ;;
#  bsd*)     echo "BSD" ;;
#  msys*)    echo "WINDOWS" ;;
#  *)        echo "unknown: $OSTYPE" ;;
#esac


if [[ "$ANSWER" =~ ^Y ]] 
then
    echo "
THE FOLLOWING WILL BE CHECKED AND INSTALLED:
    - sqlite3
    - sqlite3   (python module)
    - hashlib   (python module)
    - platform  (python module)
    - blessings (python module)

<< PRESS ENTER TO CONTINUE >>"
read

YUM=`which yum`
APT_GET=`which apt-get`
PACMAN=`which pacman`
APTITUDE=`which aptitude`
ZYPPER=`which zypper`
CHECK1=`python -c "import sqlite3"`
CHECK2=`python -c "import hashlib"`
CHECK3=`python -c "import platform"`
CHECK4=`python -c "import blessings"`


check()
{
    if [[ "$CHECK1" != 0 ]]; then
        pip install sqlite3
    fi     
    if [[ "$CHECK2" != 0 ]]; then
        pip install hashlib
    fi
    if [[ "$CHECK3" != 0 ]]; then
        pip install platform
    fi
    if [[ "$CHECK4" != 0 ]]; then
        pip install blessings
    fi
}


    if [[ ! -z $YUM ]]
    then
        sudo yum install sqlite
        check
    elif [[ ! -z $APT_GET ]]
    then
        sudo apt-get install sqlite3
        check
    elif [[ ! -z $PACMAN ]]
    then
        sudo pacman -S sqlite3
        check
    elif [[ ! -z $ZYPPER ]]
    then
        sudo zypper -S sqlite3
        check
    else
        echo "I gotta add in another option for your package manager, sorry..."
        exit 1
    fi
fi

cd  SCRIPTS/
./pyinbash.sh

