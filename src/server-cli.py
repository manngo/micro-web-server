#!/usr/bin/python3
# -*- coding: utf-8 -*-
from server import startServer, stopServer
from settings import JSONSettings
import sys, os, argparse, webbrowser, threading

helpMessage = '''
Micro Web Server
© Mark Simon
https://github.com/manngo/micro-web-server/

Usage:

	MicroWebServer [-h | --host] HOST [-p | --port] PORT [-g | --go] [-s | --save] "PROJECT NAME" [path]

Arguments:

	-h, --host		Host Name	(Original Default: localhost)
	-p, --port		Port Number	(Original Default: 8000)

	-s, --save		Saves Settings as "Project Name"
	-r, --read		Reads Settings from "Project Name"
					This ignores the path, host and port settings
	-d, --delete	Deletes Settings "Project Name"
					This ignores the path, host and port settings

	-g, --go		Open URL in Default Browser

	--help			This Help Message

	(path)			Directory to be Served

					Omitted:	Show Help
					.		 	Use Current Directory
					-		 	Use Saved Directory from Last Time

The host, port and path, whether set or default, will be saved for next time.
'''

helpMessage= helpMessage.expandtabs(4)

#	Prefs
prefsPath = os.path.join(os.path.expanduser('~'), '.micro-web-server', 'prefs.json')
prefs = JSONSettings(prefsPath, {
	'default': {'path': os.getcwd(), 'host': 'localhost', 'port': 8000},
	'saved': {},
}, force=False)

#	Arguments

parser = argparse.ArgumentParser(
	description='Micro Web Server',
	prog='MicroWebServer',
	formatter_class=argparse.ArgumentDefaultsHelpFormatter,
	add_help=False
)

parser.add_argument('-h', '--host', help='Host', default=prefs['default']['host'], dest='host')
parser.add_argument('-p', '--port', help='Port Number', default=prefs['default']['port'], dest='port', type=int)

parser.add_argument('-s', '--save', help='Save Settings', dest='save')
parser.add_argument('-r', '--read', help='Read Settings', dest='read')
parser.add_argument('-d', '--delete', help='Delete Settings', dest='delete')

parser.add_argument('-g', '--go', help='Open URL in Browser', action='store_true', dest='go')
parser.add_argument('--help', help='Help', action='store_true', dest='help')

parser.add_argument('path', nargs='?', help='Select Directory')

args = parser.parse_args()

if args.help or args.path is None:
	print(helpMessage)
	sys.exit()

print(args.path, args.host, args.port, args.save, args.read, args.delete, args.go)

if args.path == '.':
	args.path = os.getcwd()
elif args.path == '-':
	args.path = prefs['default']['path']

saved = { k.lower(): k for k in prefs['saved'] }

if args.read is not None:
	if args.read.lower() not in saved:
		print('{} not saved; using defaults'.format(args.read))
	else:
		args.read = saved[args.read.lower()]
		args.path, args.host, args.port = (prefs['saved'][args.read][k] for k in ('path', 'host', 'port'))

if args.save is not None:
	if args.save.lower() in saved:
		del prefs['saved'][saved[args.save.lower()]]
	prefs['saved'][args.save] = {'path': args.path, 'host': args.host, 'port': args.port}
	prefs.write()

if args.delete is not None:
	if args.delete.lower() in saved:
		del prefs['saved'][saved[args.delete.lower()]]
	prefs.write()

print(args)

prefs['default'] = {'path': args.path, 'host': args.host, 'port': args.port}
prefs.write()

os.chdir(args.path)

def goServer():
	print('Going to:\nhttp://{}:{}'.format(args.host, int(args.port)))
	webbrowser.open('http://{}:{}'.format(args.host, int(args.port)))

if args.go: threading.Timer(2, goServer).start()

#stopServer();
startServer(args.path, args.host, args.port)

print('Bye Bye')
