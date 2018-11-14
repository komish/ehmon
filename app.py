#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys

import conf as c

from flask import Flask
from flask import request
from flask import Response
from pathlib import Path

app_name = "EhMon!"

app = Flask(app_name)

"""set configuration-driven variables."""
cookie_dir = c.cookie_dir
secret_key = c.secret_key

def do_thing(directory, cookiename=".trigger"):
    """do a thing when triggered."""

    """
    In this sample case, we touch a cookie file
    but this action could be anything at all
    """
    pth = "{}/{}".format(directory, cookiename)
    # we assume write permissions
    Path(pth).touch()
    return True

@app.route("/trigger", methods=["POST"])
def trigger():
    """listen and receive an authenticated trigger.""" 
    resp = Response(status=401)

    # expect json request data
    r = request.get_json()
    if r.__contains__('secret_key') and str(r['secret_key']) == str(secret_key):
        do_thing(cookie_dir)
        resp.status_code = 202
    return resp

def main():
    return app.run(host=c.listen_address, port=c.listen_port)
    
if __name__ == "__main__":
    sys.exit(main())
