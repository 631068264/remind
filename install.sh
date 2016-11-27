#!/usr/bin/env bash

rm -r .env/
rm -r .git/
rm -r .idea/

virtualenv -p python3.5 .env/
source .env/bin/activate
pip install -r requirements.txt
deactivate

sudo cp conf/supervisor_remind.conf /etc/supervisor/conf.d
sudo supervisorctl reload
sudo supervisorctl status

sudo nginx -s stop
sudo nginx -c `pwd`/conf/nginx_remind.conf
RESULT=$?
if [ $RESULT -ne 0 ]; then
  echo "Nginx start fail!"
  exit 1
fi

ps aux|grep nginx
