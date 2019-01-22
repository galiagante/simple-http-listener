# Simple HTTP Listener

This service application is meant for quick, low-volume HTTP testing use GET, HEAD and POST methods. It was originally intended for uses with Github Webhooks as a test end-point, but has numerous other uses.

Note: This app DOES NOT CURRENTLY SUPPORT SSL, although this may be addressed in future versions. A good workaround for this problem is to use 'haproxy' for SSL termination, and pointing at this listener as a 'backend'.

Regardless, be mindful about leakage of potentially sensitive information during the use of the app. Remember: "When in doubt, don't send it out!"

## Warnings

This service app is for testing only! Under no cirsumstances should this application be left facing the public Internet or any other uncontrolled network without appropriate supervision and additional layers of protection. It should be shutdown immedaitely after testing is completed.

## Prerequisites

This application requires only Python 2.7.x and uses only built-in modules and libraries, with the exception of 'simplejson'.

## Getting Started

There is no installation, per se. Simply clone this repo locally:

```
$ git clone https://github.com/galiagante/simple-http-listener
```

Once cloned, you may edit '' and update the following variable to suit your use case:
* 'ADDR' is the IP address or FQDN for your server
* 'PORT' is any open port numbers you wish, assuming no conflicts or blockages via firewall(s)
* 'TOKEN' is an arbitrary string used for authenticating POST requests.

A simple token can be generated like so:
```
$ openssl enc -aes-256-ctr -k $(cat /dev/urandom | tr -dc 'a-zA-Z0-9-_@#*()_+{}|:<>?=' | \
  fold -w 1024 | head -n 1) -P -md sha256
```
I would suggest using the 'key' value. Note that token string matching IS case sensitive.

## Usage:

For HEAD requests:
```
$ curl --head http://your_fqdn.com[:port_number]/
```

For GET requests (to serve a default 'index.html' supplied with this appp):
```
$ curl http://your_fqdn.com[:port_number]/
```

For POST requests (remember to set the 'TOKEN' value):
```
$ curl -H "Content-Type: application/json" -H "X-TOKEN: [token_string]" -X POST \
  -d '{"key":"abc","value":"xyz"}' http://your_fqdn.com[:port_number]
```
Or...
```
$ curl -H "Content-Type: application/json" -H "X-TOKEN: [token_string]" -X POST \
  -d @filename.json  http://your_fqdn.com[:port_number]
```

POST'd data is assumed to be JSON and will be written to a local file. If other formats are needed, you can edit the source code accordingly.

## Deployment

This should be be usable as a stand-alone application almost anywhere Python 2.7.x is available. 

## Built With

* [Python](https://www.python.org) - The web framework used

## Authors

* **Rick Pelletier** - rpelletier@gannett.com

See also the list of [contributors](https://github.com/your/project/contributors) who participated in this project.

## License

This project consists solely of public-domain source code and is therefore free of any ownership or copyright restrictions.
