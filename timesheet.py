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


def main():
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
                    exec_cmd = active_window_cmd.strip()
                    runner = subprocess.Popen(exec_cmd, shell=True, 
                             stdin=subprocess.PIPE, stdout=subprocess.PIPE)
                    if get_idle_time() > 8:
                        application = ''
                    else:
                        application = runner.communicate()[0][:-1]
            else:
                application = win32gui.GetWindowText(win32gui.GetForegroundWindow())

            print timestamp, application
            logging.debug(timestamp + "|" + application)
            count+=ONE_TICK
 

if __name__ == "__main__":
    main()


