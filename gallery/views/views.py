# -*- coding: utf-8 -*-
import hashlib

from flask import request

from gallery.main import app


@app.route('/wx')
def main_handler():
    signature = request.args.get('signature')
    timestamp = request.args.get('signature')
    nonce = request.args.get('nonce')
    echostr = request.args.get('echostr')
    token = 'MemoryGallery'
    ls = [token, timestamp, nonce]
    ls.sort()
    sha1 = hashlib.sha1()
    map(sha1.update, ls)
    hashcode = sha1.hexdigest()
    print "handle/GET func: hashcode, signature: ", hashcode, signature
    if hashcode == signature:
        return echostr
    else:
        return ""
