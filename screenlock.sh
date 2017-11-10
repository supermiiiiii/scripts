#!/bin/bash
if [[ $(hostname) == "aphrodite" ]]; then
	cd /home/bryan/Dropbox/logs/aphrodite-motion
	N=30
	M=0
else
	cd /home/bryan/motion
	N=300
	M=5
fi

echo $$ > /tmp/lock.pid
trap 'rm /tmp/lock.pid' EXIT

(sleep $N && motion) &
PID=$!

ham stop

scrot /tmp/screenshot.png
convert /tmp/screenshot.png -blur 0x5 /tmp/screenshotblur.png
i3lock -n -i /tmp/screenshotblur.png

kill $PID
pkill motion

touch -t $(date --date="$M minutes ago" +%Y%m%d%H%M) /tmp/motionts
find . -newer /tmp/motionts -type f -delete
find . -name "*.avi" -size -100k -delete
