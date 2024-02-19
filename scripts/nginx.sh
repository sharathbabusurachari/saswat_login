#!/bin/bash

sudo cp -rf app.conf /etc/nginx/sites-available/saswat_cust_app
chmod 710 /var/lib/jenkins/workspace/04_Saswat_login_CICD

if [ ! -e /etc/nginx/sites-enabled/saswat_cust_app ]; then
    # Create the symbolic link
    sudo ln -s /etc/nginx/sites-available/saswat_cust_app /etc/nginx/sites-enabled/saswat_cust_app

fi

sudo nginx -t

sudo systemctl start nginx
sudo systemctl enable nginx

echo "Nginx has been started"

sudo systemctl status nginx