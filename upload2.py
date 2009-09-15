#!/usr/bin/python
from datetime import datetime
for f in open('31May2009-Sun.timesheet').readlines():
    a = f.split('|')
    d=datetime.strptime(a[0], "%a, %d %b %Y %H:%M:%S")
    p = d.strftime("%Y-%m-%d %H:%M:%S")
    print 'curl -u lparthsarathy:z "http://127.0.0.1:8000/api/upload.yaml" -F  "application=%s" -F "timestamp=%s"' % (a[1], p)

