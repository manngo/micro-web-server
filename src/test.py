#!/Library/Frameworks/Python.framework/Versions/3.9/bin/python3
# -*- coding: utf-8 -*-

import tkinter
from tkinter import ttk
window = tkinter.Tk()
testEntry = ttk.Entry(window)
testEntry.bind('<FocusOut>', lambda event: print(event.widget.get()))
testEntry.grid(column=0,row=0)
thingEntry = ttk.Entry(window)
thingEntry.bind('<FocusOut>', lambda event: print(event.widget.get()))
thingEntry.grid(column=0,row=1)
startButton = ttk.Button(window,text='OK',command=lambda: print('click'))
startButton.grid(column=0,row=2, sticky='W')

window.mainloop()
print('Bye Bye')
