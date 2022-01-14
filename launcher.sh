#!/bin/sh
# launcher.sh
# navigate to home directory, then to this directory, then execute python script, then back home

#cd /
#cd home/pi/
#sudo python3 start.py >> /home/pi/logs/gpslogs.txt
#cd /
#nohup

if ! pgrep -f 'main.py'
then
    python3 /home/pi/pitracker/main.py 2>> errlogs.txt

# run the test, remove the two lines below afterwards
else
    echo "running"
fi
