. $HOME/spaCy/.env/bin/activate
cd $HOME/cfb/AWS/website
touch access.log
sudo chmod 777 access.log
gunicorn -w 1 -b 0.0.0.0:5000 --access-logfile=access.log webserver:app