#Author: Brian Rico
#Date: 02/18/2018
#Purpose: when the program runs, it will need arguments

if [ $1 = "id"]; then
   >&2 echo "id"

elif [ $1 = "author" ]; then
    echo "Brian Rico"
else
    echo "too many line arguements"
fi;

if [ -d $1]
