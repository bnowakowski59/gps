# Instalacja

## Biblioteki
```console
$ sudo rapsi-config

---> Interfacing options --> Serial --> "Would you like a logging shell ..." - No --> "Would you like the serial port ..." - Yes

$ sudo apt-get install git
$ git clone https://github.com/bnowakowski59/raspberryGSM.git

$ sudo apt-get install python3-pip

$ python3 -m pip uninstall serial

$ sudo -H pip3 install pyserial

$ sudo -H pip3 install python-pppd

$ sudo -H pip3 install pymongo

$ sudo nano /boot/config.txt

---> enable_uart=1
---> dtoverlay=disable-wifi
```

## Minicom

```console
$ sudo apt-get install minicom
$ sudo minicom -b 115200 -D /dev/ttyS0
```

## GPRS and ppp

```console

$ sudo apt-get install ppp screen elinks
$ sudo -i
$ cd /etc/ppp/peers
$ cp provider gprs
$ sudo nano gprs
```
### gprs file
* Wklej zawartość do pliku `gprs`:
```sh
# See the manual page pppd(8) for information on all the options.

# MUST CHANGE: replace myusername@realm with the PPP login name given to
# your by your provider.
# There should be a matching entry with the password in /etc/ppp/pap-secrets
# and/or /etc/ppp/chap-secrets.

# MUST CHANGE: replace ******** with the phone number of your provider.
# The /etc/chatscripts/pap chat script may be modified to change the
# modem initialization string.
connect "/usr/sbin/chat -v -f /etc/chatscripts/gprs -T internet"

# Serial device to which the modem is connected.
/dev/ttyS0

# Speed of the serial line.
115200

nocrtscts

debug

nodetach
ipcp-accept-local
#ipcp-accept-remote
# Assumes that your IP address is allocated dynamically by the ISP.
noipdefault
# Try to get the name server addresses from the ISP.
usepeerdns
# Use this connection as the default route.
defaultroute

# Makes pppd "dial again" when the connection is lost.
persist

# Do not ask the remote to authenticate.
noauth

```

## ZeroTier
```console
curl -s https://install.zerotier.com | sudo bash
```

## Autostart
* Nadaj prawa do pliku `launcher.sh`
```console
$ chmod 755 launcher.sh
```
* sprawdz poprawność działania pliku `launcher.sh`
```console
$ sh launcher.sh
```
* Włączenie autostartu pliku `launcher.sh`
```console
$ sudo crontab -e

* * * * * sh /home/pi/launcher.sh
```

* I2C
```console
lsmod | grep rtc
$ sudo rmmod rtc-ds1307
sudo i2cdetect -y 1