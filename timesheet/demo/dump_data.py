#!/usr/bin/python
from demoprofile.models import Chunk
from datetime import datetime
import time
from django.contrib.auth.models import User


u = User.objects.filter(username='lparthsarathy')[0]

for each_line in open('31May2009-Sun.timesheet').readlines():
    fields = each_line.split('|')
    epoch_time = time.strptime(fields[0], "%a, %d %b %Y %H:%M:%S")
    app_name = unicode(fields[1].strip(), errors='ignore')
    c = Chunk(timestamp=datetime.fromtimestamp(time.mktime(epoch_time)), application=app_name, person=u)
    c.save()



