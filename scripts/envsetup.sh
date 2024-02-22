#!/bin/bash

cd $WORKSPACE
if [ -d "saswatfinenv" ]
then
    echo "Python virtual environment exists." 
else
    python3 -m venv saswatfinenv

fi

echo $PWD
source saswatfinenv/bin/activate
python3 manage.py makemigrations
python3 manage.py migrate


pip3 install -r $WORKSPACE/requirements.txt


if [ -d "logs" ] 
then
    echo "Log folder exists." 
else
    mkdir logs
    touch logs/error.log logs/access.log
fi

sudo chmod -R 777 logs