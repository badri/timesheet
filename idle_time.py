#!/usr/bin/python
import ctypes
import os

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
xss.XScreenSaverAllocInfo.restype = ctypes.POINTER(XScreenSaverInfo)
xss_info = xss.XScreenSaverAllocInfo()
xss.XScreenSaverQueryInfo( dpy, root, xss_info)
print "Idle time in milliseconds: %d" % ( xss_info.contents.idle, )
