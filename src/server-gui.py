#!/usr/bin/python3
# -*- coding: utf-8 -*-
from server import startServer, stopServer

import os
import tkinter
from tkinter.filedialog import askdirectory
from tkinter import messagebox

oldpath = os.getcwd()

def start():
	global okButton
	okButton.config(text='Stop',command=stop)
	okButton
	path = pathText.get()
	host = hostText.get()
	port = int(portText.get())
	os.chdir(path)

	startServer(path,host,port,True);

def stop():
	global okButton
	stopServer();
	okButton.config(text='Start',command=start)

def setFolder():
	path = tkinter.filedialog.askdirectory(title='Serve Folder:')
	if path != '':
		pathText.delete(0,"end")
		pathText.insert(0,path)

def exit():
	if messagebox.askokcancel('Quit','Quit?'):
		stopServer()
		window.destroy()

bgcolour = '#123456'
fgcolour = 'white'

window = tkinter.Tk()
window.title('Hello')
#window.geometry('350x200')
window.configure(bg=bgcolour)
window.protocol('WM_DELETE_WINDOW',exit)

headingLabel = tkinter.Label(window, text="Micro Web Server", bg=bgcolour, fg=fgcolour, font=("Source Sans Pro",24))
headingLabel.grid(columnspan=2,row=0, sticky='WE',padx=8,pady=2)


pathLabel = tkinter.Label(window, text="Path", bg=bgcolour, fg=fgcolour)
pathLabel.grid(column=0,row=1, sticky='W',padx=8,pady=2)
pathText = tkinter.Entry(window)
#pathText.insert(0,'.')
pathText.insert(0,oldpath)
pathText.grid(columnspan=2,row=2, sticky='WE',padx=8,pady=2)

pathButton = tkinter.Button(window,text='...', bg=bgcolour, fg=fgcolour,command=setFolder)
pathButton.grid(column=2,row=2, padx=8,pady=8, sticky='E')


hostLabel = tkinter.Label(window, text="Host", bg=bgcolour, fg=fgcolour)
hostLabel.grid(column=0,row=3, sticky='W',padx=8,pady=2)
hostText = tkinter.Entry(window)
hostText.insert(0,'localhost')
hostText.grid(column=0,row=4,padx=8,pady=2)

portLabel = tkinter.Label(window, text="Port", bg=bgcolour, fg=fgcolour)
portLabel.grid(column=1,row=3, sticky='W',padx=8,pady=2)
portText = tkinter.Entry(window)
portText.insert(0,'8000')
portText.grid(column=1,row=4,padx=8,pady=2)

okButton = tkinter.Button(window,text='Start', bg=bgcolour, fg=fgcolour,command=start)
okButton.grid(column=2,row=4, padx=8,pady=8, sticky='E')

window.mainloop()
print(42)
