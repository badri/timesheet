#!/usr/bin/python
from datetime import datetime
import subprocess
import re

pd = open('processed_data', 'w')

for f in open('31May2009-Sun.timesheet').readlines()[120:240]:
    a = f.split('|')
    d=datetime.strptime(a[0], "%a, %d %b %Y %H:%M:%S")
    ts = d.strftime("%Y-%m-%d %H:%M:%S")
    app = re.sub('\"', '\\"', a[1])    
    entry = "%s ::: %s\n" % (ts.strip(), app.strip())
    pd.write(entry)

pd.close()

cmd = 'curl -u lparthsarathy:z "http://127.0.0.1:8000/api/upload.json" -F  "upload=%s"' % (open('processed_data').read())
print cmd
exec_cmd = cmd.strip()
runner = subprocess.Popen(exec_cmd, shell=True, 
                               stdin=subprocess.PIPE, stdout=subprocess.PIPE)


