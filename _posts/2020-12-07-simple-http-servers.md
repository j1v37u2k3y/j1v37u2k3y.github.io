---
layout: post
title: HTTP(S) Servers for File Transfer in Linux
categories: admin
tags: [notes, linux, file-transfer, http-server, python-server, php-server, nginx, python, php]
published: true
author: j1v37u2k3y
show_sidebar: true
toc: true
searchable: true
---
I cannot tell you how many times I needed to have a quick and dirty way to transfer files in an engagement, so here are some that I have used before.

<!--cut-->

![banner.png](/assets/images/simple-http-servers/banner.png)
{:.center-image}

Local -- 10.10.10.1, remote -- 10.10.10.2.

# Python
Python can help out in almost any situation, and our case is no exception.

Everyone knows these great commands for starting HTTP servers for the second version of python:
```text
local@server:~$ python -m SimpleHTTPServer [port]
```

Also this:
<https://gist.github.com/tnory56/1e734b74c2cf64d9d9e86c36280bc4ad>

And its analog for Python 3:

```text
local@server:~$ python3 -m http.server [-h] [--cgi] [--bind ADDRESS] [port]
```

In this way, you can only pull files from where the server was raised, since the only methods that it understands out of the box are `HEAD` and `GET`.
However, no one forbids us to slightly modify the default behavior by adding, for example, handling `POST` (displaying the contents to the console for example) and `PUT` requests.

Simple script:
```python
#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Usage: python3 SimpleHTTPServer+.py [-h] [--bind ADDRESS] [port]

import http.server
import os

from argparse import ArgumentParser


class HTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
	def _set_headers(self):
		self.send_response(200)
		self.send_header('Content-type', 'text/html')
		self.end_headers()

	def do_POST(self):
		content_length = int(self.headers['Content-Length'])
		post_data = self.rfile.read(content_length)
		self._set_headers()
		self.wfile.write(b'<html><body><h1>POST!</h1></body></html>')

		print(post_data.decode('utf-8'))

	def do_PUT(self):
		path = self.translate_path(self.path)
		if path.endswith('/'):
			self.send_response(405, 'Method Not Allowed')
			self.wfile.write(b'PUT not allowed on a directory\n')
			return
		else:
			try:
				os.makedirs(os.path.dirname(path))
			except FileExistsError: pass
			length = int(self.headers['Content-Length'])
			with open(path, 'wb') as f:
				f.write(self.rfile.read(length))
			self.send_response(201, 'Created')
			self.end_headers()


def cli_options():
	parser = ArgumentParser()

	parser.add_argument(
		'--bind',
		'-b',
		default='',
		metavar='ADDRESS',
		help='Specify alternate bind address [default: all interfaces]'
	)

	parser.add_argument(
		'port',
		action='store',
		default=8000,
		type=int,
		nargs='?',
		help='Specify alternate port [default: 8000]'
	)

	return parser.parse_args()


if __name__ == '__main__':
	args = cli_options()
	http.server.test(HandlerClass=HTTPRequestHandler, port=args.port, bind=args.bind)
```

Allows to successfully both *upload and download files*:
```text
local@server:~$ wget 10.10.10.2:8881/message
--2018-10-11 10:51:35--  http://10.10.10.2:8881/message
Connecting to 10.10.10.2:8881... connected.
HTTP request sent, awaiting response... 200 OK
Length: 10 [application/octet-stream]
Saving to: ‘message’

message              100%[===================>]      10  --.-KB/s    in 0s

2018-10-11 10:51:35 (2.40 MB/s) - ‘message’ saved [10/10]
```

```text
local@server:~$ cat message
Hi there!
```

```text
remote@server:~$ python3 SimpleHTTPServer+.py 8881
Serving HTTP on 0.0.0.0 port 8881 (http://0.0.0.0:8881/) ...
10.10.10.1 - - [11/Oct/2018 11:04:37] "GET /message HTTP/1.1" 200 -
```

So to *upload* to a Linux machine:
```text
local@server:~$ curl --upload-file message 10.10.10.2:8881
  % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
                                 Dload  Upload   Total   Spent    Left  Speed
100    10    0     0  100    10      0      9  0:00:01  0:00:01 --:--:--     9


local@server:~$ curl -d @message -X POST 10.10.10.2:8881
<html><body><h1>POST!</h1></body></html>
```

```text
remote@server:~$ python3 SimpleHTTPServer+.py 8881
Serving HTTP on 0.0.0.0 port 8881 (http://0.0.0.0:8881/) ...
10.10.10.1 - - [11/Oct/2018 10:52:10] "PUT /message HTTP/1.1" 201 -
10.10.10.1 - - [11/Oct/2018 10:52:18] "POST / HTTP/1.1" 200 -
Hi there!
```

```text
remote@server:~$ cat message
Hi there!
```

Available methods: `GET`,` POST`, `PUT`


## Python 3 SSL Server

- simple-https-server.py

```python
# taken from http://www.piware.de/2011/01/creating-an-https-server-in-python/
# generate server.xml with the following command:
#    openssl req -new -x509 -keyout /tmp/key.pem -out /tmp/cert.pem -days 365 -nodes
# run as follows:
#    python simple-https-server.py
# then in your browser, visit:
#    https://localhost:443

from http.server import HTTPServer, SimpleHTTPRequestHandler
import ssl


httpd = HTTPServer(('<your-ip>', 443), SimpleHTTPRequestHandler)

httpd.socket = ssl.wrap_socket(httpd.socket, keyfile='/tmp/key.pem', certfile='/tmp/cert.pem', server_side=True)

httpd.serve_forever()
```

- You can use a higher port e.g.:4443 so you can run as a normal user


# PHP
Unsurprisingly, a two-line *PHP* script can solve all our problems - the "hypertext preprocessor" after all :sunglasses:

So, for a trivial PHP server, we need code like this:
```php
<?php
$fname = basename($_REQUEST['filename']);
file_put_contents('uploads/' . $fname, file_get_contents('php://input'));
?>
```

In the screenshot below (clickable) you can see the entire procedure for starting the server: preliminary settings on the panel on the left, tests on the right.

[![php.png](/assets/images/simple-http-servers/php.png)](/assets/images/simple-http-servers/php.png)
{:.center-image}

A few words about what's going on here:
 1. Create the necessary directories and a script with the content above.
 2. Create a user from which the server will spin. The new user is needed so that enemies cannot execute the code that they themselves upload. Therefore, with the command `umask 555`, we set the setting for access rights issued to all new files that our user will create. `555` is` 777 XOR 222`, so the default bits will be set as if we manually set `chmod 222` to each new file (only write allowed).
 3. We start the server and test it.
 4. **???????**
 5. PROFIT

Available methods: `GET`,` POST`, `PUT`

# Nginx

So where can we go without *the High-Performance Web Server and Reverse Proxy*?
Fortunately, on most Linux distributions *Nginx* is preinstalled, so it can be configured and deployed in a matter of minutes.

Again, in the screenshot below, you can see the entire launch procedure: preliminary settings on the panel at the top, tests at the bottom.

[![nginx.png](/assets/images/simple-http-servers/nginx.png)](/assets/images/simple-http-servers/nginx.png)
{:.center-image}

What's going on here:
1. Create the necessary directories and server configuration based on the sample from `default '(the contents of the config are below).
2. Make the config active (symlink in `/etc/nginx/sites-enabled/`)
3. Restart the `nginx` service, check its activity and test the server.
4. **???????**
5. PROFIT

Config file:
```text
root@kali:~# cat /etc/nginx/sites-available/file_upload
server {
	listen 8881 default_server;
	server_name jiveturkey.top;
	location / {
		root                  /var/www/uploads;
		dav_methods           PUT;
		create_full_put_path  on;
    		dav_access            group:rw all:r;
	}
}
```

How to use it, do not forget to stop the server:

```text
root@kali:~# systemctl stop nginx
```

Available methods: `GET`,` PUT`.


### SPECIAL THANKS TO [snovvcrash.rocks](https://snovvcrash.rocks/){:target="_blank"} For this post but slightly modified
