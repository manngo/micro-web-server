import os, sys, webbrowser, json

from library import dbug
from server import startServer, stopServer
from settings import JSONSettings
import tkform
import styles

#	import tkinter
from tkinter.filedialog import askdirectory
from tkinter import messagebox, simpledialog
#from tkinter import ttk
import tkinter.font

#	Prefs
prefsPath = os.path.join(os.path.expanduser('~'), '.micro-web-server', 'prefs.json')
prefs = JSONSettings(prefsPath, {
	'default': {'path': os.getcwd(), 'host': 'localhost', 'port': 8000},
	'saved': {},
}, force=False)

#	Support Functions
def getProjects():
	saved = prefs['saved']
	projects = {'Default': prefs['default']} | prefs['saved']
	return projects

def updateProjects(name):
	projects = getProjects()
	projectsCombo['values'] = list(projects.keys())
	if name:
		projectsCombo.current(projectsCombo['values'].index(name))
	else:
		projectsCombo.current(0)
	selectProject()

def saveAsProject():
	name = simpledialog.askstring('Save Project', 'Save Project as:')
	if name:
		name = name.lower()
		saveProject(name)
		updateProjects(name)

def saveProject(project=None):
	if not project:
		project = projectVar.get()
	details = {'path': pathVar.get(), 'host': hostVar.get(), 'port': int(portVar.get())}
	prefs['saved'][project] = details
	prefs.write()

def deleteProject():
	if projectsCombo.current() == 0:
		return	#	Can’t delete default
	name = projectsCombo.get()
	if not messagebox.askyesno(f'Delete {name}', f'Are you sure you want to delete {name}?'):
		return
	if name in prefs['saved']:
		del prefs['saved'][name]
		prefs.write()
		updateProjects(None)
	#	projectsCombo.current(0)

#	Form Functions
def setLaunch(*args):
	launchVar.set(f'http://{hostVar.get()}:{portVar.get()}')

def selectProject():
	values = projects[projectVar.get()]
	pathVar.set(values['path'])
	hostVar.set(values['host'])
	portVar.set(values['port'])
#	setLaunch()

def setFolder():
	filePath = tkinter.filedialog.askdirectory(title='Serve Folder:')
	if filePath != '':
		pathVar.set(filePath)

def close():
	if True or messagebox.askokcancel('Quit', 'Do you want to quit Micro Web Server?'):
		stopServer()
		form.destroy()

#	Server Functions
def start(*args):
	path = pathVar.get()
	host = hostVar.get()
	port = int(portVar.get())
	try:
		os.chdir(path)
		startServer(path, host, port, True)
		setLaunch()
		startButton.config(text='Stop', command=stop)
	except OSError as e:
		messagebox.showerror(title='Path not Found', message=f'There is no directory at:\n\n{path}\n\nThe Server cannot be started')

def stop(*args):
	stopServer()
	startButton.config(text='Start', command=start)
	launchVar.set('')

#	Initialise
oldpath = os.getcwd()
projects = getProjects()

#	Window
form = tkform.TKForm('Micro Web Server')
form.configure(background="#ECECEC", padx=12, pady=12)
form.title('Micro Web Server')
#form.geometry('350x200')
form.protocol('WM_DELETE_WINDOW', close)
(labelFont, headingFont, entryFont, linkFont, linkHoverFont) = styles.init(form)
#styles.init(form)

#	Dynamic Variables
projectVar = tkinter.StringVar(form)
pathVar = tkinter.StringVar(form)
hostVar = tkinter.StringVar(form)
portVar = tkinter.StringVar(form)
launchVar = tkinter.StringVar(form)

#	Layout Variables
startButton = tkform.OKButton(form, 'Start', command=start)
projectsCombo = tkform.Combobox(form, items=list(projects.keys()), textvariable=projectVar, default='md', command=selectProject)

#	Layout
layout = {
	'Server': [
		[tkform.BoldLabel(form, text='Micro Web Server', foreground='#133796', font=headingFont), True, True, True, True],
		['Projects', True, None, None, tkform.Label(form, text='Test')],
		[
			projectsCombo, True,
			tkform.Button(form, 'Save', saveProject),
			tkform.Button(form, 'Save As …', command=saveAsProject),
			tkform.Button(form, 'Delete …', deleteProject)
		],
		['Path', True, True, True, None],
		[
			tkform.Textbox(form, textvariable=pathVar), True, True, True,
			tkform.Button(form, 'Select …', command=setFolder)
		],
		['Host', True, True, 'Port', None],
		[
			tkform.Textbox(form, textvariable=hostVar), True, True,
			tkform.Textbox(form, textvariable=portVar) ,
			startButton
		],
		['Open in Browser:', tkform.LinkLabel(form, textvariable=launchVar), True, True],
	],
	'About': [
		[tkform.BoldLabel(form, text='About Micro Web Server', foreground='#133796', font=headingFont), True, True,
		 True, True],
		['© Mark Simon', True, True, True, True],
		[tkform.LinkLabel(form, text="https://github.com/manngo/micro-web-server/", style='link.TLabel'), True, True,
		 True, True],
	]
}
form.doLayout(layout)
selectProject()

form.show()
