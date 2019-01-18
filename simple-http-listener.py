#!/usr/bin/env python
# -*- coding: utf-8 -*-

# silly http listener, version 0.4-20190117-beta (do not distribute)
# by rick pelletier (galiagante@gmail.com), jan 2019

from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import SocketServer
import simplejson
import random
import datetime

# global server parameters
ADDR="0.0.0.0" # string: IP or FQDN of your test installation
PORT=8000 # integer: any port you like. be aware of port conflicts and/or firewall issues
TOKEN="[change me]" # string: for authenticating POST requests

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

        if 'X-TOKEN' in self.headers:
            if self.headers['X-TOKEN'] == TOKEN:
                self.data_string = self.rfile.read(int(self.headers['Content-Length']))
                self.send_response(200)
                self.end_headers()

                print "Matching token: " + self.headers['X-TOKEN']
                data = simplejson.loads(self.data_string)
                uniq_filename = str(datetime.datetime.now().date()) + '_' + str(datetime.datetime.now().time()).replace(':', '.')
                # POST'd data is expected to be a JSON object
                with open(uniq_filename + ".json", "w") as outfile:
                    simplejson.dump(data, outfile)
                print "{}".format(data)
            else:
                self.send_response(403)
                self.end_headers()
        else:
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
