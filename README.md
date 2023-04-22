Interesting SEO thread: https://twitter.com/alex_buraks/status/1618988134850785280?cxt=HHwWgMDTlbDI5vcsAAAA https://twitter.com/alex_buraks/status/1619370810959093760
- don't have numbers in your URL
- do have keywords in your URL
- title is important (not from that article)
- website as a whole plays a part. It would be good to consolidate where possible.
- Google analytics JS
- Advertisments
- "Pages with low quality content affect the entire domain."
- Percentage of caps in title
- Links from Wikipedia
- Links from homepage
- Less than 3 pages from "home page"

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
sudo cp mbmblog.service /etc/systemd/system/
sudo systemctl start mbmblog
sudo systemctl enable mbmblog
sudo systemctl status mbmblog

# nginx settings
# Make sure you add blog.co-pinion.com and www.blog.co-pinion.com A records to DNS manager
sudo certbot --nginx -d  blog.co-pinion.com -d www.blog.co-pinion.com
# See below for mbmblog listing
sudo vim /etc/nginx/sites-available/mbmblog
sudo ln -s /etc/nginx/sites-available/mbmblog /etc/nginx/sites-enabled/
sudo systemctl restart nginx
# Should now be accessible at:
https://www.blog.co-pinion.com/#home
https://blog.co-pinion.com/#home
```

Your nginx should look like this after figuring out letsencrypt
```
server {
    root /var/www/html;
    server_name  blog.co-pinion.com www.blog.co-pinion.com;

    listen 443 ssl; # managed by Certbot

    # RSA certificate
    ssl_certificate /etc/letsencrypt/live/co-pinion.com/fullchain.pem; # managed by Certbot
    ssl_certificate_key /etc/letsencrypt/live/co-pinion.com/privkey.pem; # managed by Certbot

    include /etc/letsencrypt/options-ssl-nginx.conf; # managed by Certbot

    # Redirect non-https traffic to https
    if ($scheme != "https") {
        return 301 https://$host$request_uri;
    } # managed by Certbot

    location / {
        include proxy_params;
        proxy_pass http://unix:/home/mbm/mbmblog/TeaUponTweed.github.io.sock;
    }
    # ^^^^ IMPORTANT PART ^^^^^^^^^

}

server {
    if ($host = www.blog.co-pinion.com) {
        return 301 https://$host$request_uri;
    } # managed by Certbot


    if ($host = blog.co-pinion.com) {
        return 301 https://$host$request_uri;
    } # managed by Certbot


    listen 80 default_server;
    listen [::]:80 default_server;
    server_name  blog.co-pinion.com www.blog.co-pinion.com;
    return 404; # managed by Certbot
}

```

TODO
- Firewall setup, use ufw but only allow localhost on weird internal ports
- Figure out cacheing https://www.nginx.com/blog/nginx-caching-guide/ + maybe cloudflare
