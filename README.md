Adapted from https://www.digitalocean.com/community/tutorials/how-to-serve-flask-applications-with-gunicorn-and-nginx-on-ubuntu-18-04
```bash
# setup system
sudo apt update
sudo apt install python3-pip python3-dev build-essential libssl-dev libffi-dev python3-setuptools
sudo apt install python3-venv

# git repo
git clone git@github.com:TeaUponTweed/TeaUponTweed.github.io.git
cd ~/TeaUponTweed.github.io
# setup python
python3 -m venv python_venv
source python_venv/bin/activate
pip install wheel
pip install gunicorn flask

# run
gunicorn --bind 0.0.0.0:5001 wsgi:app

# create service
sudo echo "
[Unit]
Description=Gunicorn instance to serve mbm blog
After=network.target

[Service]
User=mbm
Group=www-data
WorkingDirectory=/home/mbm/TeaUponTweed.github.io
Environment="PATH=/home/mbm/TeaUponTweed.github.io/python_venv/bin"
ExecStart=/home/mbm/TeaUponTweed.github.io/python_venv/bin/gunicorn --workers 3 --bind unix:TeaUponTweed.github.io.sock -m 007 wsgi:app

[Install]
WantedBy=multi-user.target
" > /etc/systemd/system/mbmblog.service

sudo systemctl start mbmblog
sudo systemctl enable mbmblog
sudo systemctl status mbmblog

```

TODO
- Firewall setup, use ufw but only allow localhost on weird internal ports
