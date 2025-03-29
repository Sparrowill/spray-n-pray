# Python Venv #

The system is running a python venv inside the repo structure. This is a python3 thing and means we can use pip to install packages.

Before you can use the venv in a session, you must activate it. 

Being inisde the ui folder, open a terminal 

``` bash
pi@gamepi:~/Documents/spray-n-pray/ui $  source /home/pi/Documents/spray-n-pray/ui//bin/activate
```

You can now run python commands normally
``` bash
pi@gamepi:~/Documents/spray-n-pray/ui $  python test.py
```


Or use ./launcher.sh inside the home/pi directory