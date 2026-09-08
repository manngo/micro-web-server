#	References
#	https://docs.python.org/3/library/tkinter.html
#	https://docs.python.org/3/library/tkinter.ttk.html#ttk-styling
#	https://www.pythontutorial.net/tkinter/ttk-style/

import tkinter
from tkinter import ttk
import sys

def init(form):
#	Fonts
	labelFont = ('TkTextFont', 12, 'bold')
	headingFont = ('TkTextFont', 24, 'bold')
	comboboxFont = ('TkTextFont', 10, 'bold')
	entryFont = ('TkFixedFont', 10, 'normal')
	linkFont = ('TkTextFont', 12, 'normal')
	linkHoverFont = ('TkTextFont', 12, 'normal underline')

#	ttk Styles
	ttk.Style().configure('TLabel', foreground='#133796', font=labelFont)
	ttk.Style().configure('heading.TLabel', foreground="#133796", font=headingFont)
	ttk.Style().configure('link.TLabel', foreground='#133796', font=linkFont)
	ttk.Style().configure('link.hover.TLabel', foreground='#133796', font=linkHoverFont)
	ttk.Style().configure('TListbox', weight='normal', font=comboboxFont)
	form.option_add('*TCombobox*Listbox.font', comboboxFont)  # apply font to combobox list

	if sys.platform == 'darwin': ttk.Style().configure('active.TButton', foreground='white')

	return (labelFont, headingFont, entryFont, linkFont, linkHoverFont)