#!/usr/bin/python
"""
* Thomas Gouverneur - 2015
"""
import requests
import json
import sys
import time
import hashlib
from passlib.hash import pbkdf2_sha256

def saltPassword(password, username):
  now = int(time.time())
  first = pbkdf2_sha256.encrypt('test123', salt=username, rounds=20000)
  print first
  second = hashlib.sha256(first + str(now)).hexdigest()
  return second

url = 'http://127.0.0.1:5080/login'
data = {}
data['username'] = 'tgouverneur'
data['password'] = saltPassword('test123', data['username'])

headers = {'content-type': 'application/json'}

r = requests.Session()
resp = r.post(url, data=json.dumps(data), headers=headers)
try:
   print '[-] JSON response:'
   print resp.json()
except:
   print '[!] An error has occured'

