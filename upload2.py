#!/usr/bin/python
from datetime import datetime
import subprocess
import re
import sys

pd = open('processed_data', 'w')
print sys.argv[1]
for f in open(sys.argv[1]).readlines():
    a = f.split('|')
    print a
    d=datetime.strptime(a[0], "%a, %d %b %Y %H:%M:%S")
    ts = d.strftime("%Y-%m-%d %H:%M:%S")
    app = re.sub('\"', '\\"', a[1])    
    entry = "%s ::: %s\n" % (ts.strip(), app.strip())
    pd.write(entry)

pd.close()

from jsonrpc.proxy import ServiceProxy
#s = ServiceProxy('http://localhost:8000/json/')
s = ServiceProxy('http://timedefrag.com/json/')
s.userprofile.upload('lakshminp', 'zaqwer123', open('processed_data').read())

