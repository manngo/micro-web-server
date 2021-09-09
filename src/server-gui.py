#!/Library/Frameworks/Python.framework/Versions/3.9/bin/python3
# -*- coding: utf-8 -*-

#	References
#	https://docs.python.org/3/library/tkinter.html
#	https://docs.python.org/3/library/tkinter.ttk.html#ttk-styling
#	https://www.pythontutorial.net/tkinter/ttk-style/

#	Imports
from server import startServer, stopServer, loadPrefs, savePrefs, initPrefs

import os, sys, webbrowser, json

import tkinter
from tkinter.filedialog import askdirectory
from tkinter import messagebox, simpledialog
from tkinter import ttk
import tkinter.font

#	Functions
def getProjects():
	saved = [k for k in prefs['saved']]
	projects = ['Default',*saved]
	return (saved,projects)

def start():
	global startButton, launchLink, prefs
	startButton.config(text='Stop',command=stop)
	#startButton
	path = pathText.get()
	host = hostText.get()
	port = int(portText.get())
	#prefs = {'path': path, 'host': host, 'port': port}
	os.chdir(path)
	startServer(path,host,port,True);
	#savePrefs()
	launchLink.config(text='http://{}:{}'.format(host,port))

def stop():
	global startButton
	stopServer();
	startButton.config(text='Start',command=start)
	launchLink.config(text='')

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
	webbrowser.open(event.widget['text'])

def linkify(widget):
	widget.bind('<Button-1>', lambda event: webbrowser.open(event.widget['text']))
	widget.bind("<Enter>", lambda event: event.widget.configure(style='link.hover.TLabel'))
	widget.bind("<Leave>", lambda event: event.widget.configure(style='link.TLabel'))

def updateProjects():
	global saved, projects, projectsCombo
	saved,projects = getProjects()
	projectsCombo['values'] = projects

def saveAsProject(name=None):
	#global prefs, saved, projectsCombo
	if not name: name = simpledialog.askstring('Save Project','Save Project as:')
	#if name==None: print('None')
	#if name=='': print('empty string')
	#if name: print(f'Result: {name}')
	if name.lower() in saved:
		del prefs['saved'][saved[name.lower()]]
	prefs['saved'][name] = {'path': pathText.get(), 'host': hostText.get(), 'port': int(portText.get())}
	savePrefs()
	updateProjects()
	projectsCombo.current(projectsCombo['values'].index(name))

def saveProject():
	saveAsProject(projectsCombo.get())

def deleteProject():
	if projectsCombo.current() == 0: return	#	Can’t delete default
	name = projectsCombo.get()
	if not messagebox.askyesno(f'Delete {name}',f'Are you sure you want to delete {name}?'): return
	if name in saved:
		del prefs['saved'][name]
	savePrefs()
	updateProjects()
	projectsCombo.current(0)

def loadProject():
	if projectsCombo.current() == 0:
		path,host,port = (prefs['default'][k] for k in ('path','host','port'))
	else:
		project = projectsCombo.get();
		path,host,port = (prefs['saved'][project][k] for k in ('path','host','port'))
	pathText.delete(0,"end")
	pathText.insert(0,path)
	hostText.delete(0,"end")
	hostText.insert(0,host)
	portText.delete(0,"end")
	portText.insert(0,port)

def readProject(event):
	loadProject()
	pass

#	Initialise
oldpath = os.getcwd()
prefs = initPrefs()
saved,projects = getProjects()

#	Window
window = tkinter.Tk()
window.configure(background="#ECECEC", padx=12, pady=12)
window.title('Micro Web Server')
#window.geometry('350x200')
window.protocol('WM_DELETE_WINDOW',exit)

notebook = ttk.Notebook(window)
notebook.pack(expand=True)
mainFrame = ttk.Frame(notebook)
mainFrame.pack(fill='both',expand=True)
notebook.add(mainFrame, text='Server')
infoFrame = ttk.Frame(notebook)
infoFrame.pack(fill='both',expand=True)
notebook.add(infoFrame, text='About')

#	Appearance
padding = {'padx': 8, 'pady': 2}

#	Fonts
labelFont = tkinter.font.nametofont("TkTextFont")
labelFont.config(weight='bold', size=12)
headingFont = labelFont.copy()
headingFont.config(size=24)
comboboxFont = labelFont.copy()
comboboxFont.config(weight='normal', size=12)
entryFont = tkinter.font.nametofont("TkFixedFont")
entryFont.config(size=12)
linkFont = entryFont.copy()
linkFont.config(weight='normal', underline=False)
linkHoverFont = entryFont.copy()
linkHoverFont.config(weight='bold', underline=True)

#	ttk Styles
ttk.Style().configure('TLabel',foreground="#666666", font=labelFont)
ttk.Style().configure('heading.TLabel', foreground='#133796', font=headingFont)
ttk.Style().configure('link.TLabel',foreground='#133796',font=linkFont)
ttk.Style().configure('link.hover.TLabel',foreground='#133796',font=linkHoverFont)
ttk.Style().configure('TListbox',weight='normal', font=comboboxFont)
window.option_add('*TCombobox*Listbox.font', comboboxFont)   # apply font to combobox list

if sys.platform=='darwin': ttk.Style().configure('active.TButton',foreground='white')

#	Info
infoLabels = [
	ttk.Label(infoFrame, text="About Micro Web Server", style="heading.TLabel"),
	ttk.Label(infoFrame, text="© Mark Simon"),
	ttk.Label(infoFrame, text="Open:"),
	ttk.Label(infoFrame, text="https://github.com/manngo/micro-web-server/", style='link.TLabel'),
]
infoGrid = [
	{'column':0, 'row':0, 'columnspan':2, 'sticky':'W'},
	{'column':0, 'row':1, 'columnspan':2, 'sticky':'W'},
	{'column':0, 'row':2, 'sticky':'W'},
	{'column':1, 'row':2, 'sticky':'W'},
]
for i,v in enumerate(infoLabels): v.grid(**infoGrid[i])
linkify(infoLabels[3])

#	Heading
headingLabel = ttk.Label(mainFrame, text="Micro Web Server", style="heading.TLabel")
headingLabel.grid(columnspan=8,row=0, sticky='WE')

#	Projects
projectsLabel = ttk.Label(mainFrame, text="Projects")
projectsLabel.grid(column=0,row=1, sticky='W')
projectsCombo = ttk.Combobox(mainFrame, font=comboboxFont)
projectsCombo['state'] = 'readonly'
updateProjects()
projectsCombo.current(0)
projectsCombo.grid(columnspan=3, column=0,row=2, sticky='W')
projectsCombo.bind('<<ComboboxSelected>>',readProject)

saveButton = ttk.Button(mainFrame,text='Save', command=saveProject)
saveButton.grid(column=3,row=2, sticky='E')
saveAsButton = ttk.Button(mainFrame,text='Save As …', command=saveAsProject)
saveAsButton.grid(column=4,row=2, sticky='E')
deleteButton = ttk.Button(mainFrame,text='Delete …', command=deleteProject)
deleteButton.grid(column=5,row=2, sticky='E')

#	Path
pathLabel = ttk.Label(mainFrame, text="Path")
pathLabel.grid(column=0,row=3, sticky='W')
pathText = ttk.Entry(mainFrame, font=entryFont)
pathText.insert(0,prefs['default']['path'])
pathText.bind('<FocusOut>', lambda event: savePrefs(path=event.widget.get()))
pathText.grid(columnspan=5,row=4, sticky='WE')

pathButton = ttk.Button(mainFrame,text='Select …', command=setFolder)
pathButton.grid(column=5,row=4, sticky='E')

#print(prefs)
#print(prefs['default'])
#print(prefs['default']['path'])

#	Host
hostLabel = ttk.Label(mainFrame, text="Host")
hostLabel.grid(column=0,row=5, sticky='W')
hostText = ttk.Entry(mainFrame, font=entryFont)
hostText.insert(0,prefs['default']['host'])
hostText.bind('<FocusOut>', lambda event: savePrefs(host=event.widget.get()))
hostText.grid(columnspan=3, column=0, row=6, sticky='W')

#	Port
portLabel = ttk.Label(mainFrame, text="Port")
portLabel.grid(columnspan=2, column=3,row=5, sticky='W',padx=8,pady=2)
portText = ttk.Entry(mainFrame, font=entryFont)
portText.insert(0,prefs['default']['port'])
portText.bind('<FocusOut>', lambda event: savePrefs(port=int(event.widget.get())))
portText.grid(columnspan=2, column=3,row=6)

#	Start
startButton = ttk.Button(mainFrame,text='Start', default="active", style="active.TButton", command=start)
startButton.grid(column=5,row=6, sticky='E')

#	Launch
launchLabel = ttk.Label(mainFrame, text="Open in Browser:")
launchLabel.grid(column=0,row=7, sticky='W', pady=(8,4))
launchLink = ttk.Label(mainFrame, text='', style='link.TLabel')
launchLink.grid(columnspan=4, column=1,row=7, sticky='W', pady=(8,4))
linkify(launchLink)

#	Main
window.mainloop()
print('Bye Bye')
