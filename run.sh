# get the drive name
DRIVE=$(lsblk --list --noheadings --paths --output KNAME,LABEL | grep BILDSCHIRM | awk '{print }')
if [ $DRIVE = "" ]; then
    echo Could not find drive
    exit 127
fi

# mount the drive to /media/bildschirm
pmount -r $DRIVE bildschirm

# sync Pipfile.lock
pipenv sync

# disable the mouse by hiding it when unused
unclutter -idle 0 &

# run the slideshow
pipenv run main.py
