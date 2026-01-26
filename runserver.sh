pip install WeasyPrint Pango Cairo

cd erb8ProjShop
source venv/bin/activate
python manage.py runserver
# python manage.py createsuperuser
# python manage.py makemigrations

# python manage.py migrate
# python manage.py collectstatic

# sudo systemctl start gunicorn
# sudo systemctl enable gunicorn

cd ~
sudo nano /etc/nginx/sites-available/myproject
server {
    listen 80;
    # server_name your_server_ip_or_domain;
    server_name django.natureai.dpdns.org;
    
    location = /favicon.ico { access_log off; log_not_found off; }
    location /static/ {
        root /home/smarts_ricky/erb8ProjShop;
    }

    location / {
        include proxy_params;
        proxy_pass http://unix:/run/gunicorn.sock;
    }
}


cd ~
sudo nano /etc/systemd/system/gunicorn.service

[Unit]
Description=gunicorn daemon
After=network.target

[Service]
User=smarts_ricky
Group=www-data
WorkingDirectory=/home/smarts_ricky/erb8ProjShop
ExecStart=/home/smarts_ricky/erb8ProjShop/venv/bin/gunicorn \
          --access-logfile - \
          --workers 3 \
          --bind unix:/run/gunicorn.sock \
          erb8ProjShop.wsgi:application

[Install]
WantedBy=multi-user.target


sudo systemctl start gunicorn
sudo systemctl enable gunicorn


sudo ln -s /etc/nginx/sites-available/myproject /etc/nginx/sites-enabled
sudo nginx -t
sudo systemctl restart nginx