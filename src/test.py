#!/Library/Frameworks/Python.framework/Versions/3.9/bin/python3
# -*- coding: utf-8 -*-

import tkinter
from tkinter import ttk

def addShortcutKeys(entry):
	def selectAll(event):
		event.widget.select_range(0,'end')
	entry.bind('<Control-a>',selectAll)



def doSomething(event):
	text = event.widget.get()
	print(text)

window = tkinter.Tk()
testEntry = ttk.Entry(window)
testEntry.bind('<FocusOut>', doSomething)
testEntry.grid(column=0,row=0)
#addShortcutKeys(testEntry)
thingEntry = ttk.Entry(window)
thingEntry.bind('<FocusOut>', doSomething)
thingEntry.grid(column=0,row=1)
startButton = ttk.Button(window,text='OK',command=lambda: print('click'))
startButton.grid(column=0,row=2, sticky='W')

window.mainloop()
print('Bye Bye')
