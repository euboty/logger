#!/usr/bin/env bash

set -x

# install system depedencies
apt-get update
apt-get install -y nginx sqlite3 python3-pip

# enable i2c for gyroscope
modprobe i2c_bcm2835
modprobe i2c_dev
if ! grep -q "vibration sensor config" /etc/modules; then
    tee -a /etc/modules << END

# vibration sensor config
i2c_bcm2835
i2c_dev
END
fi


# enable temperature sensor on PIN 4
modprobe wire
modprobe w1-gpio
modprobe w1-therm

if ! grep -q "temperature sensor config" /etc/modules; then
    tee -a /etc/modules << END

# temperature sensor config
wire
w1-gpio
w1-therm
END
fi

if ! grep -q "temperature sensor config" /boot/config.txt; then
    tee -a /boot/config.txt << END

# temperature sensor config
dtoverlay=w1-gpio
gpiopin=4
pullup=on
END
fi

python3 -m pip install -r requirements.txt

cp ./gunicorn.service /etc/systemd/system/
systemctl enable gunicorn

cp ./logger.nginx.conf /etc/nginx/sites-enabled/
rm /etc/nginx/sites-enabled/default
systemctl reload nginx

python3 ../database.py create
