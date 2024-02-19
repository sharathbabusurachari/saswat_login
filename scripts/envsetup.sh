#!/bin/bash

cd $WORKSPACE
if [ -d "otp_env" ]
then
    echo "Python virtual environment exists." 
else
    python3 -m venv otp_env
fi

echo $PWD
source otp_env/bin/activate


pip3 install -r $WORKSPACE/requirements.txt

if [ -d "logs" ] 
then
    echo "Log folder exists." 
else
    mkdir logs
    touch logs/error.log logs/access.log
fi

sudo chmod -R 777 logs