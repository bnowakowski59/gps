#!/bin/sh
# installer.sh will install the necessary packages to get the gifcam up and running with 
# basic functions

# Install packages
PACKAGES="git python3-pip minicom ppp screen elinks"
sudo apt-get update && sudo apt-get upgrade -y
sudo apt-get install $PACKAGES -y
sudo python3 -m pip uninstall serial
sudo -H pip3 install pyserial
sudo -H pip3 install python-pppd
sudo -H pip3 install pymongo
sudo -H pip3 install interruptingcow
sudo -H pip3 install adafruit-circuitpython-mpu6050
curl -s https://install.zerotier.com | sudo bash