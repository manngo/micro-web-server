#!/Library/Frameworks/Python.framework/Versions/3.9/bin/python3
# -*- coding: utf-8 -*-

#	References
#	https://docs.python.org/3/library/tkinter.html
#	https://docs.python.org/3/library/tkinter.ttk.html#ttk-styling
#	https://www.pythontutorial.net/tkinter/ttk-style/

from server import startServer, stopServer

import os, sys, webbrowser, json

import tkinter
from tkinter.filedialog import askdirectory
from tkinter import messagebox
from tkinter import ttk

prefsPath = os.path.join(os.path.expanduser('~'),'.micro-web-server','prefs.json')

oldpath = os.getcwd()

def loadPrefs(defaults):
	data = {}
	if os.path.isfile(prefsPath):
		jsonFile = open(prefsPath,'r')
		try:
			data = json.load(jsonFile)
		except Exception:
			pass
		jsonFile.close()
	print(data)
	return data

def savePrefs(path=None,host=None,port=None):
	global prefs
	if path: prefs['path'] = path
	if host: prefs['host'] = host
	if port: prefs['port'] = port

	print(prefs)
	os.makedirs(os.path.dirname(prefsPath),exist_ok=True)
	jsonFile = open(prefsPath,'w')
	json.dump(prefs,jsonFile)
	jsonFile.close()
	return prefs

defaults = {'path': oldpath, 'host': 'localhost', 'port': 8000}
prefs = { **defaults, **loadPrefs(defaults) }
print(prefs)
savePrefs()

def start():
	global startButton, launchLink, prefs
	startButton.config(text='Stop',command=stop)
	startButton
	path = pathText.get()
	host = hostText.get()
	port = int(portText.get())
	prefs = {'path': path, 'host': host, 'port': port}
	os.chdir(path)
	startServer(path,host,port,True);
	savePrefs()
	launchLink.config(text='http://{}:{}'.format(host,port))

def stop():
	global startButton
	stopServer();
	startButton.config(text='Start',command=start)

def setFolder():
	path = tkinter.filedialog.askdirectory(title='Serve Folder:')
	if path != '':
		pathText.delete(0,"end")
		pathText.insert(0,path)

def exit():
	if messagebox.askokcancel('Quit','Quit?'):
		stopServer()
		window.destroy()

def launchURL(event):
	host = hostText.get()
	port = int(portText.get())
	webbrowser.open('http://{}:{}'.format(host,port))

#	Window
window = tkinter.Tk()
window.configure(background="#ECECEC", padx=12, pady=12)
window.title('Micro Web Server')
#window.geometry('350x200')
window.protocol('WM_DELETE_WINDOW',exit)

#	Appearance
padding = {'padx': 8, 'pady': 2}
if sys.platform=='darwin': ttk.Style().configure('active.TButton',foreground='white')
ttk.Style().configure('TLabel',font=("Source Sans Pro",14,'bold'),foreground="#666666")
ttk.Style().configure('link.TLabel',foreground='#133796')

#	Heading
headingLabel = ttk.Label(window, text="Micro Web Server", font=("Source Sans Pro",24))
headingLabel.grid(columnspan=2,row=0, sticky='WE')

#	Path
pathLabel = ttk.Label(window, text="Path")
pathLabel.grid(column=0,row=1, sticky='W')
pathText = ttk.Entry(window)
pathText.insert(0,prefs['path'])
pathText.bind('<FocusOut>', lambda event: savePrefs(path=event.widget.get()))
pathText.grid(columnspan=4,row=2, sticky='WE')

pathButton = ttk.Button(window,text='Select …', command=setFolder)
pathButton.grid(column=4,row=2, sticky='E')

#	Host
hostLabel = ttk.Label(window, text="Host")
hostLabel.grid(column=0,row=3, sticky='W')
hostText = ttk.Entry(window)
hostText.insert(0,prefs['host'])
hostText.bind('<FocusOut>', lambda event: savePrefs(host=event.widget.get()))
hostText.grid(columnspan=2, column=0, row=4, sticky='W')

#	Port
portLabel = ttk.Label(window, text="Port")
portLabel.grid(column=2,row=3, sticky='W',padx=8,pady=2)
portText = ttk.Entry(window)
portText.insert(0,prefs['port'])
portText.bind('<FocusOut>', lambda event: savePrefs(port=int(event.widget.get())))
portText.grid(columnspan=2, column=2,row=4)

#	Start
startButton = ttk.Button(window,text='Start', default="active", style="active.TButton", command=start)
startButton.grid(column=4,row=4, sticky='E')

#	Launch
launchLabel = ttk.Label(window, text="Open in Browser:")
launchLabel.grid(column=0,row=5, sticky='W', pady=(8,4))
launchLink = ttk.Label(window, text='', style='link.TLabel')
launchLink.grid(column=1,row=5, sticky='W', pady=(8,4))
launchLink.bind('<Button-1>', launchURL)

#	Main
window.mainloop()
print('Bye Bye')
