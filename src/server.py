#!/Library/Frameworks/Python.framework/Versions/3.9/bin/python3
# -*- coding: utf-8 -*-

#	References
#	https://python.readthedocs.io/en/v2.7.2/library/simplehttpserver.html
#	https://docs.python.org/3/library/http.server.html
#	https://stackabuse.com/serving-files-with-pythons-simplehttpserver-module/


import http.server, socketserver, os, json, sys
import threading

httpd = None
oldpath = os.getcwd()


def resourcePath(path):
	try:
		base = sys._MEIPASS
	except Exception:
		base = os.path.abspath('.')

def loadPrefs():
	data = {}
	if os.path.isfile(prefsPath):
		jsonFile = open(prefsPath,'r')
		try:
			data = json.load(jsonFile)
		except Exception:
			pass
		jsonFile.close()
	#print(data)
	return data

def savePrefs(name=None,path=None,host=None,port=None):
	global prefs
	if name==None:
		if path: prefs['default']['path'] = path
		if host: prefs['default']['host'] = host
		if port: prefs['default']['port'] = port
	else:
		if path: prefs['saved'][name]['path'] = path
		if host: prefs['saved'][name]['host'] = host
		if port: prefs['saved'][name]['port'] = port
	#print(prefs)
	os.makedirs(os.path.dirname(prefsPath),exist_ok=True)
	jsonFile = open(prefsPath,'w')
	json.dump(prefs,jsonFile)
	jsonFile.close()
	return prefs

def initPrefs():
	return prefs

prefsPath = os.path.join(os.path.expanduser('~'),'.micro-web-server','prefs.json')

defaults = {
	'default': {'path': oldpath, 'host': 'localhost', 'port': 8000},
	'saved': {}
}

prefs = { **defaults, **loadPrefs() }
savePrefs()


class SimpleHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
	def do_GET(self):
		try:
			http.server.SimpleHTTPRequestHandler.do_GET(self)
		except IOError:
			print ('oops');

def startServer(path,host,port,gui=False):
	global httpd, oldpath
	handler = SimpleHTTPRequestHandler

	if gui:
		httpd = http.server.ThreadingHTTPServer((host,port), handler)
		thread = threading.Thread(target = httpd.serve_forever)
		thread.daemon = True
	else:
		httpd = socketserver.TCPServer((host,port), handler)

	message = 'Serving {}\nat: {}:{}'
	#print(message.format(path,host or 'localhost',port))

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
