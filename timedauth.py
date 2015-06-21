import json
import hashlib
import time
from functools import wraps
from flask import Flask, abort, request, Response

site_username = 'tgouverneur'
site_password = hashlib.sha256('test123').hexdigest()
skew_seconds = 15

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

app = Flask(__name__)

@app.route("/login", methods=['POST'])
@wrapresponse
def login():
    params = request.json
    if not 'username' in params or not 'password' in params:
	return {'rc':-1, 'msg':'Missing username or password'}

    if params['username'] != site_username:
	return {'rc':-1, 'msg':'Wrong username'}
        
    rc = checkPassword(params['password'])

    if rc is False:
	return {'rc':-1, 'msg':'Wrong password or clock skewed'}

    return {'rc':0, 'skew':rc, 'msg':'Successfuly logged in'}



if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5080, debug=True)

