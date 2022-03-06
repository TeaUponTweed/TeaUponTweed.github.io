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
```

TODO
- Firewall setup, use ufw but only allow localhost on weird internal ports
