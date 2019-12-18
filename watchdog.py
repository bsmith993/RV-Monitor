#!/usr/bin/python
import psutil
import sys
import subprocess



# For RV monitor
for process in psutil.process_iter():
    if process.cmdline() == ['python', '/home/pi/v2.py']:
         sys.exit('Process found: exiting.')

subprocess.Popen(['python', '/home/pi/v2.py'])


