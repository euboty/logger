#!/usr/bin/env bash

set -x

# install system depedencies
apt-get update
apt-get install -y nginx sqlite3 python3-pip

# enable i2c for gyroscope
modprobe i2c_bcm2835
modprobe i2c_dev
echo "" >> /etc/modules
echo "# vibration sensor config" >> /boot/config.txt
echo "i2c_bcm2835" >> /etc/modules
echo "i2c_dev" >> /etc/modules

# enable temperature sensor on PIN 4
modprobe wire
modprobe w1-gpio
modprobe w1-therm
echo "" >> /etc/modules
echo "# temperature sensor config" >> /boot/config.txt
echo "wire" >> /etc/modules
echo "w1-gpio" >> /etc/modules
echo "w1-therm" >> /etc/modules

echo "" >> /boot/config.txt
echo "# temperature sensor config" >> /boot/config.txt
echo "dtoverlay=w1-gpio" >> /boot/config.txt
echo "gpiopin=4" >> /boot/config.txt
echo "pullup=on" >> /boot/config.txt

python3 -m pip install -r requirements.txt

cp ./gunicorn.service /etc/systemd/system/
systemctl enable gunicorn

cp ./logger.nginx.conf /etc/nginx/sites-enabled/
rm /etc/nginx/sites-enabled/default
service nginx reload

python3 ../database.py create
