#!/usr/bin/python
"""
* Thomas Gouverneur - 2015
"""
import json
import hashlib
from passlib.hash import pbkdf2_sha256
import time
from functools import wraps
from flask import Flask, abort, request, Response

app = Flask(__name__)

site_username = 'tgouverneur'
site_password = pbkdf2_sha256.encrypt('test123', salt=site_username, rounds=20000)
skew_seconds = 15

@app.after_request
def after_request(resp):
    resp.headers.add('Access-Control-Allow-Origin', '*')
    resp.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    resp.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE')
    return resp

def checkPassword(password):
    now = int(time.time())

    # first check it against NOW
    if hashlib.sha256(site_password + str(now)).hexdigest() == password:
        return 0
   
    # allow skew_seconds below/above NOW
    for i in range(1, skew_seconds):
      if hashlib.sha256(site_password + str(now - i)).hexdigest() == password:
          return (0 - i)
   
      if hashlib.sha256(site_password + str(now + i)).hexdigest() == password:
          return i

    return False

def wrapresponse(f):
    @wraps(f)
    def wrapperfunc(*args, **kwargs):
        if not request.data:
            abort(400)
        resp = f(*args, **kwargs)
        return Response(json.dumps(resp),200,[("Content-Type","application/json")])
    return wrapperfunc


@app.route("/login", methods=['POST'])
@wrapresponse
def login():
    params = request.json
    if not 'username' in params or not 'password' in params:
	return {'rc':-1, 'msg':'Missing username or password'}

    if params['username'] != site_username:
	return {'rc':-1, 'msg':'Wrong username'}
        
    app.logger.debug('REQ: ' + params['password'])
    rc = checkPassword(params['password'])

    if rc is False:
	return {'rc':-1, 'msg':'Wrong password or clock skewed'}

    return {'rc':0, 'skew':rc, 'msg':'Successfuly logged in'}



if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5080, debug=True)

