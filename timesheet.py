#!/usr/bin/python
 
import platform
import ctypes
import os

if platform.uname()[0] != 'Linux':
    import win32gui
else:
    import subprocess

import time
import logging

from datetime import datetime
import subprocess
import re

USER = 'lparthsarathy'
PASSWD = 'z'
UPLOAD_URL = 'http://127.0.0.1:8000/api/upload.json'

# globals
log_file_name = time.strftime("%d%b%Y-%a", time.localtime()) + '.timesheet'        

# logging.basicConfig(level=logging.DEBUG,
#                     format='%(message)s',
#                     filename=log_file_name,
#                     filemode='w')

ONE_TICK = 10
TOTAL_TICKS = 24*60*60
count = 0
UPLOAD_TIME = ONE_TICK * 6 # 1 min

track_uploads = 0
PROCESSED_FILE = 'processed_data'


if platform.uname()[0] == 'Linux':
    class XScreenSaverInfo( ctypes.Structure):
      """ typedef struct { ... } XScreenSaverInfo; """
      _fields_ = [('window',      ctypes.c_ulong), # screen saver window
                  ('state',       ctypes.c_int),   # off,on,disabled
                  ('kind',        ctypes.c_int),   # blanked,internal,external
                  ('since',       ctypes.c_ulong), # milliseconds
                  ('idle',        ctypes.c_ulong), # milliseconds
                  ('event_mask',  ctypes.c_ulong)] # events

    xlib = ctypes.cdll.LoadLibrary( 'libX11.so.6')
    dpy = xlib.XOpenDisplay( os.environ['DISPLAY'])
    root = xlib.XDefaultRootWindow( dpy)
    xss = ctypes.cdll.LoadLibrary( 'libXss.so.1')

    def get_idle_time():
        xss.XScreenSaverAllocInfo.restype = ctypes.POINTER(XScreenSaverInfo)
        xss_info = xss.XScreenSaverAllocInfo()
        xss.XScreenSaverQueryInfo( dpy, root, xss_info)
        # print "Idle time in milliseconds: %d" % ( xss_info.contents.idle, )
        return xss_info.contents.idle/1000
    active_window_cmd = """
    xprop -id `xprop -root |awk '/_NET_ACTIVE_WINDOW/ {print $5; exit;}'` |awk -F = '/WM_NAME/ {print $2; exit;}' | sed 's/^ "//g' | sed 's/"$//g'
    """

def process_log_contents():
    global PROCESSED_FILE, log_file_name
    pd = open(PROCESSED_FILE, 'w')
    for f in open(log_file_name).readlines():
        a = f.split('|')
        d=datetime.strptime(a[0], "%a, %d %b %Y %H:%M:%S")
        ts = d.strftime("%Y-%m-%d %H:%M:%S")
        app = re.sub('\"', '\\"', a[1])    
        entry = "%s ::: %s\n" % (ts.strip(), app.strip())
        pd.write(entry)

    print "processed file read:"
    print open(PROCESSED_FILE).read()


def upload_to_server():
    global UPLOAD_URL, USER, PASSWD, PROCESSED_FILE, log_file_name
    print "processed file read:"
    print open(PROCESSED_FILE).read()
    cmd = 'curl -u %s:%s "%s" -F  "upload=%s"' % (USER, PASSWD, UPLOAD_URL, open(PROCESSED_FILE).read())
    print cmd
    exec_cmd = cmd.strip()
    runner = subprocess.Popen(exec_cmd, shell=True, 
                                   stdin=subprocess.PIPE, stdout=subprocess.PIPE)

def clear_logs():
    global log_file_name
    open(log_file_name, 'w').write('')


def main():
    global TOTAL_TICKS, ONE_TICK, count, track_uploads, UPLOAD_TIME
    while True: #forever        
        while count < TOTAL_TICKS:
            f=open(log_file_name, 'a')
            time.sleep(ONE_TICK)
            timestamp = time.strftime("%a, %d %b %Y %H:%M:%S", time.localtime())
            if platform.uname()[0] == 'Linux':
                    exec_cmd = active_window_cmd.strip()
                    runner = subprocess.Popen(exec_cmd, shell=True, 
                             stdin=subprocess.PIPE, stdout=subprocess.PIPE)
                    if get_idle_time() > 8:
                        application = ''
                    else:
                        application = runner.communicate()[0][:-1]
            else:
                application = win32gui.GetWindowText(win32gui.GetForegroundWindow())

            f.write(timestamp + "|" + application + "\n")

            print "log file:"
            print open(log_file_name).read()

            count+=ONE_TICK
            track_uploads+=ONE_TICK
            if track_uploads == UPLOAD_TIME:
                process_log_contents()
                upload_to_server()
                clear_logs()
                track_uploads = 0

 

if __name__ == "__main__":
    main()
