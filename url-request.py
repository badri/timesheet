#!/usr/bin/python
import urllib
import urllib2
 
upload_url = 'http://127.0.0.1:8000/api/upload.json'
 
 
# Create an OpenerDirector with support for Basic HTTP Authentication...
auth_handler = urllib2.HTTPBasicAuthHandler()
auth_handler.add_password(realm='TestApplication',
                          uri=upload_url,
                          user='lparthsarathy',
                          passwd='z')
opener = urllib2.build_opener(auth_handler)
# ...and install it globally so it can be used with urlopen.
urllib2.install_opener(opener)
 
values = {'application' : 'testing again via url request',
          'timestamp' : '2009-09-15 11:41:48'}
 
data = urllib.urlencode(values)
req = urllib2.Request(upload_url, data)
response = urllib2.urlopen(req)
print response
print response.read()
response = urllib2.urlopen(req)
print response
print response.read()
