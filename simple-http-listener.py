#!/usr/bin/env python
# -*- coding: utf-8 -*-

# simple http listener, version 0.5-20190122-beta (do not distribute)
# by rick pelletier (galiagante@gmail.com), jan 2019

# intended primarily for github webhook testing, but can be modified easily for other uses
# logs are written to stdout but can be redirect elsewhere, as needed

from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import os
import SocketServer
import simplejson
import random
import datetime
import hmac
import hashlib
import base64

# global server parameters
ADDR = "0.0.0.0" # string: IP or FQDN of your test installation. '0.0.0.0' means "any interface"
PORT = 81 # integer: any port you like. be aware of port conflicts and/or firewall issues
TOKEN = os.environ.get('TOKEN') # string: for authenticating POST requests

# request router(s) and supporting methods
class S(BaseHTTPRequestHandler):
    def _set_headers(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

    def do_GET(self):
        self._set_headers()
        f = open("index.html", "r")
        self.wfile.write(f.read())

    def do_HEAD(self):
        self._set_headers()

    def do_POST(self):
        self._set_headers()
        self.data_string = self.rfile.read(int(self.headers['Content-Length']))

        if 'X-Hub-Signature' in self.headers:
            if self.headers['X-Hub-Signature'] == "sha1=" + hmac.new(TOKEN, self.data_string, hashlib.sha1).digest().encode('hex'):
                self.send_response(200)
                self.end_headers()
                data = simplejson.loads(self.data_string)
                uniq_filename = str(datetime.datetime.now().date()) + '_' + str(datetime.datetime.now().time()).replace(':', '.')

                # POST'd data is expected to be a JSON object
                with open(uniq_filename + ".json", "w") as outfile:
                    simplejson.dump(data, outfile)

                print "Request accepted: Data written to " + uniq_filename + ".json"
            else:
                print "Request rejected: Incorrect token"
                self.send_response(403)
                self.end_headers()
        else:
            print "Request rejected: Missing token"
            self.send_response(403)
            self.end_headers()

        return

# base http server setup and execution
def run(server_class=HTTPServer, handler_class=S, port=PORT):
    server_address = (ADDR, port)
    httpd = server_class(server_address, handler_class)
    print 'Starting httpd...'
    # access logs will be displayed on stdout (which can be captured or redirected as desired)
    httpd.serve_forever()

# entry and exit control
if __name__ == '__main__':
    run()
    sys.exit(0)
else:
    # called externally (not supported)
    sys.exit(1)

# end of script
