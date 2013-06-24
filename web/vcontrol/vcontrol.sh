#! /bin/sh
if [ $# -eq 0 ]
then
  vboxmanage list vms | awk '{gsub(/"/,"",$1); print $1}'
  exit
fi
if [ $1 = active ]
then 
  vboxmanage list runningvms | awk '{gsub(/"/,"",$1); print $1}'
  exit
fi
if [ $1 = start ]
then
  vboxmanage startvm $2 --type headless
  echo "$2 started `date` by $3" >> /var/tmp/accessLog.tmp
  exit
fi
if [ $1 = stop ]
then
  vboxmanage controlvm $2 poweroff
  echo "$2 stopped `date` by $3" >> /var/tmp/accessLog.tmp
  exit
fi
if [ $1 = restart ]
then
  vboxmanage controlvm $2 reset
  echo "$2 restarted `date` by $3" >> /var/tmp/accessLog.tmp
  exit
fi
# TO:DO 
if [ $1 = screenshot ]
then
  vboxmanage controlvm $2 screenshotpng /var/tmp/vmscreenshot.png
  /bin/chmod 644 /var/tmp/vmscreenshot.png
  exit
fi
