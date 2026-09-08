#!/Library/Frameworks/Python.framework/Versions/3.9/bin/python3
# -*- coding: utf-8 -*-

#	References
#	https://python.readthedocs.io/en/v2.7.2/library/simplehttpserver.html
#	https://docs.python.org/3/library/http.server.html
#	https://stackabuse.com/serving-files-with-pythons-simplehttpserver-module/

#	pip3 install legacy-cgi

import http.server, socketserver, os, json, sys
import threading
#from prefs import JSONSettings, settings

httpd = None
oldpath = os.getcwd()

def resourcePath(path):
	try:
		base = sys._MEIPASS
	except Exception:
		base = os.path.abspath('.')

class SimpleHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
	def do_GET(self):
		try:
			http.server.SimpleHTTPRequestHandler.do_GET(self)
		except IOError:
			print('oops');

def startServer(path, host, port, gui=False):
	global httpd, oldpath
#	handler = http.server.SimpleHTTPRequestHandler
	handler = SimpleHTTPRequestHandler

	if gui:
		httpd = http.server.ThreadingHTTPServer((host, port), handler)
		thread = threading.Thread(target=httpd.serve_forever)
		thread.daemon = True
		print('Running')
	else:
		httpd = socketserver.TCPServer((host,port), handler)

	message = 'Serving {}\nat: {}:{}'
	#print(message.format(path, host or 'localhost', port))

	if gui:
		try:
		#	httpd.serve_forever()
			thread.start()
		except KeyboardInterrupt:
			pass
	else:
		try:
			httpd.serve_forever()
		except KeyboardInterrupt:
			stopServer()
			os.chdir(oldpath)

def stopServer():
	global httpd
	if httpd: httpd.server_close()
