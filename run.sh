# get the drive name
DRIVE=$(lsblk --list --noheadings --paths --output KNAME,LABEL | grep BILDSCHIRM | awk '{print }')
if [ $DRIVE = "" ]; then
    echo Could not find drive > run.log
    exit 127
fi

# mount the drive to /media/bildschirm
pmount -r $DRIVE bildschirm >> run.log

# disable the mouse by hiding it when unused
unclutter -idle 0 & >> run.log

# run the slideshow
pipenv run main.py
