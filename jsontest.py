#!/usr/bin/python
from jsonrpc.proxy import ServiceProxy
s = ServiceProxy('http://localhost:8000/json/')
s.userprofile.upload('badri', 'z', open('processed_data').read())

