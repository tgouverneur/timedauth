#!/usr/bin/python
import requests
import json
import sys
import time
import hashlib

def saltPassword(password):
  now = int(time.time())
  first = hashlib.sha256(password).hexdigest()
  second = hashlib.sha256(first + str(now)).hexdigest()
  return second

url = 'http://127.0.0.1:5080/login'
data = {}
data['username'] = 'tgouverneur'
data['password'] = saltPassword('test123')

headers = {'content-type': 'application/json'}

r = requests.Session()
resp = r.post(url, data=json.dumps(data), headers=headers)
try:
   print '[-] JSON response:'
   print resp.json()
except:
   print '[!] An error has occured'

