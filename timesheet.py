#!/usr/bin/python
 
import platform
if platform.uname()[0] != 'Linux':
    import win32gui
else:
    import subprocess

import time
import logging

while True: #forever
    log_file_name = time.strftime("%d%b%Y-%a", time.localtime()) + '.timesheet'        
    logging.basicConfig(level=logging.DEBUG,
                        format='%(message)s',
                        filename=log_file_name,
                        filemode='w')
    ONE_TICK = 10
    TOTAL_TICKS = 24*60*60
    count = 0
    while count < TOTAL_TICKS:
        time.sleep(ONE_TICK)    
        timestamp = time.strftime("%a, %d %b %Y %H:%M:%S", time.localtime())
        if platform.uname()[0] == 'Linux':
                exec_cmd = """xprop -id `xprop -root |awk '/_NET_ACTIVE_WINDOW/ {print $5; exit;}'` |awk -F = '/WM_NAME/ {print $2; exit;}' | sed 's/^ "//g' | sed 's/"$//g'"""
                runner = subprocess.Popen(exec_cmd, shell=True, 
                         stdin=subprocess.PIPE, stdout=subprocess.PIPE)
                application = runner.communicate()[0][:-1]
        else:
            application = win32gui.GetWindowText(win32gui.GetForegroundWindow())
        print timestamp, application
        logging.debug(timestamp + "|" + application)
        count+=ONE_TICK
 
