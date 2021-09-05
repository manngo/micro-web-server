#	References
#	https://python.readthedocs.io/en/v2.7.2/library/simplehttpserver.html
#	https://docs.python.org/3/library/http.server.html
#	https://stackabuse.com/serving-files-with-pythons-simplehttpserver-module/


import http.server, socketserver, os
import threading

httpd = None
oldpath = os.getcwd()

class SimpleHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
	def do_GET(self):
		try:
			http.server.SimpleHTTPRequestHandler.do_GET(self)
		except IOError:
			print ('oops');

def startServer(path,host,port,gui=False):
	global httpd, oldpath
	print('Path: {}\nat: {}:{}'.format(path,host,port))
	handler = SimpleHTTPRequestHandler

	if gui:
		httpd = http.server.ThreadingHTTPServer((host,port), handler)
		thread = threading.Thread(target = httpd.serve_forever)
		thread.daemon = True
	else:
		httpd = socketserver.TCPServer((host,port), handler)

	message = 'Serving {}\nat: {}:{}'
	print(message.format(path,host or 'localhost',port))

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
			print('Bye bye')

def stopServer():
	global httpd
	if httpd: httpd.server_close()
