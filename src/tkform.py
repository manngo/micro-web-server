'''
TKForm

pip3 install tkinterdnd2
'''

from library import dbug, say
import webbrowser
import platform

import tkinter
from tkinter import ttk
from tkinter.font import Font
from tkinterdnd2 import TkinterDnD

class TKForm(TkinterDnD.Tk):
	'''Main Class'''
	def __init__(self, title='GTK Window', pages=[]):
		super().__init__()
		self.title(title)

		self.pages = None
		#	self.geometry('800x720')

		if pages:
			self.addPages(pages)

		else:
			self.mainframe = ttk.Frame(self, padding='13 3 12 12')
			self.mainframe.pack(padx=8, pady=8, fill='both', expand=True)

	def addPages(self, pages=[]):
		self.notebook = ttk.Notebook(self)
		self.notebook.pack(expand=True)
		self.notebook.lower()

		self.mainframe = ttk.Frame(self.notebook, padding='13 3 12 12')

		self.notebook.add(self.mainframe, text=pages[0])
		self.pages = { pages[0]: self.mainframe }

		if len(pages) > 1:
			for i in pages[1:]:
				frame = ttk.Frame(self.notebook, padding='13 3 12 12')
				self.pages[i]= frame
				self.notebook.add(frame, text=i)

	def clear(self):
		for i in self.window.winfo_children():
			i.grid_forget()

	def addMenu(self, menu):
		cmd = 'Command' if platform.system() == 'Darwin' else 'Control'
		menubar = tkinter.Menu(self)
		self['menu'] = menubar								#	Just in case for future reference
		application_menu = None

		for name, data in menu.items():
			if callable(data):
				if not application_menu:
					application_menu = tkinter.Menu(menubar)
					menubar.insert(0, 'cascade', menu=application_menu, label=self.title())
				application_menu.add_command(label=name, command=data)
			else:
				m = tkinter.Menu(menubar)					#	New menu
				menubar.add('cascade', menu=m, label=name)		#	Add hierarchical to menu bar aka add_cascade(…)
				for name, command in data.items():				#	Add labels & commands
					name = name.split('|') + ['']
					if not name[1]:
						m.add_command(label=name[0], command=command)
					else:
						m.add_command(label=name[0], accelerator=f'{cmd}+{name[1]}', command=command)
						self.bind_all(f'<{cmd}-{name[1]}>', lambda e, fn=command: fn())

	def add(self, widget, row, column, columnspan=1, rowspan=1, sticky='W', pad=(2,2), page=None):
		self.mainframe.grid_columnconfigure(row, weight=1)
		sticky = 'nsew'
		if not page:
			dbug('=== no page ===')
			widget.grid(in_=self.mainframe, row=row, column=column, columnspan=columnspan, rowspan=rowspan, sticky=sticky, padx=pad[0], pady=pad[1])
		else:
			widget.grid(in_=self.pages[page], row=row, column=column, columnspan=columnspan, rowspan=rowspan, sticky=sticky, padx=pad[0], pady=pad[1])

	def doLayout(self, layout):
		widgets = None
		def doPage(self, page, data, items):
			for row, rowdata in enumerate(data):
				items.append([])
				previous = None
				for column, columndata in enumerate(rowdata):
					if isinstance(columndata, str):
						columndata = Label(self, text=columndata)
					if isinstance(columndata, tkinter.ttk.Widget):
						previous = columndata
						self.add(columndata, row=row + 1, column=column + 1, page=page)
						items[row].append(columndata)
					elif columndata is True and isinstance(previous, tkinter.ttk.Widget):
						columnspan = previous.grid_info()['columnspan'] + 1
						previous.grid_configure(columnspan=columnspan)
						items[row].append(None)

		if isinstance(layout, dict):
			widgets = {}
			self.addPages(pages=list(layout.keys()))
			for page, data in layout.items():
				items = []
				doPage(self, page, data, items)
				widgets[page] = items
		elif isinstance(layout, list) or isinstance(layout, tuple):
			widgets = []
			doPage(self, None, layout, widgets)
		else:
			exit('oops')

		return widgets

	def show(self):
		self.mainloop()

class Label(ttk.Label):
	def __init__(self, parent, text='', textvariable=None, command=None, **kwargs):
		self.parent = parent
		super().__init__(parent, text = text or textvariable.get(), textvariable=textvariable, **kwargs)

	def linkify(self):
		self.bind('<Button-1>', lambda event: webbrowser.open(event.widget['text']))
		self.bind("<Enter>", lambda event: event.widget.configure(style='link.hover.TLabel'))
		self.bind("<Leave>", lambda event: event.widget.configure(style='link.TLabel'))

class BoldLabel(Label):
	def __init__(self, parent, text='', textvariable=None, **kwargs):
		super().__init__(parent, text = text or textvariable.get(), textvariable=textvariable)
		self.configure(font=Font(weight='bold'))
		self.configure(**kwargs)

class LinkLabel(Label):
	def __init__(self, parent, text='', textvariable=None, **kwargs):
		super().__init__(parent, text=text, textvariable=textvariable)
		self.configure(style='link.TLabel')
		self.bind('<Button-1>', lambda event: webbrowser.open(event.widget['text']))
		self.bind("<Enter>", lambda event: event.widget.configure(style='link.hover.TLabel'))
		self.bind("<Leave>", lambda event: event.widget.configure(style='link.TLabel'))

class Textbox(ttk.Entry):
	def __init__(self, parent, textvariable=None, text=None, command=None, **kwargs):
		self.parent = parent
		self.command = command
		super().__init__(parent, textvariable=textvariable)
		self.configure(font=('TkFixedFont',))
		if text:
			self.insert(0, text)
		if command:
			self.bind('<FocusOut>', self.command)

class Textarea(tkinter.Text):
	def __init__(self, parent, height=None, width=None, text=None, command=None, **kwargs):
		self.parent = parent
		super().__init__(parent, height=height, width=width, command=command, **kwargs)
		if text:
			self.insert('0.0', text)

class Passwordbox(Textbox):
	def __init__(self, parent, textvariable=None, command=None, **kwargs):
		self.parent = parent
		super().__init__(parent, textvariable=textvariable, command=command, **kwargs)
		self.configure(show='•')

class Numberbox(Textbox):
	def check(self, value):
		try:
			value == '' or float(value)
			return True
		except:
			return False

	def __init__(self, parent, textvariable=None, text=None, command=None, **kwargs):
		super().__init__(parent, textvariable=textvariable, command=command, **kwargs)
		self.configure(validatecommand=(parent.register(self.check), '%P'), validate='key')
		if text:
			self.insert(0, text)

class Checkbox(ttk.Checkbutton):
	def __init__(self, parent, text, textvariable=None, onvalue=True, offvalue=False, **kwargs):
		super().__init__(parent, text=text, variable=textvariable, onvalue=onvalue, offvalue=offvalue, **kwargs)

class Button(ttk.Button):
	def __init__(self, parent, text, command, **kwargs):
		self.parent = parent
		super().__init__(parent, text=text, command=command, **kwargs)

class OKButton(Button):
	def __init__(self, parent, text, command, **kwargs):
		super().__init__(parent, text=text, command=command, **kwargs)
		self.configure(default='active')
		self.parent.bind('<Return>', command)
		self.parent.bind('<KP_Enter>', command)

class CancelButton(Button):
	def __init__(self, parent, text, command=None, **kwargs):
		if not command:
			command = lambda event=None: self.parent.destroy()

		super().__init__(parent, text=text, command=command, **kwargs)
		self.parent.bind('<Key-Escape>', command)
	#	self.parent.bind('<Command-.>', command)

class Combobox(ttk.Combobox):
	def __init__(self, parent, items, default=None, textvariable=None, command=None, **kwargs):
		if isinstance(items, list):
			items = [(i,i) for i in items]
		self.parent = parent
		self.items = items
		self.textvariable = textvariable
		self.command = command

		super().__init__(parent, **kwargs)

		self['values'] = [i[0] for i in items]
		default = self['values'].index(default) if default in self['values'] else 0
		default = min(max(0, int(default)), len(items) - 1)
		self.current(default)
		self.textvariable.set(items[self.current()][1])

		self.state(['readonly'])
		self.bind('<<ComboboxSelected>>', self.onSelect)

	def onSelect(self, *args):
		self.textvariable.set(self.items[self.current()][1])
		if self.command:
			self.command()


class MenuButton(ttk.OptionMenu):
	def __init__(self, parent, items, default=None, textvariable=None, **kwargs):
		self.parent = parent
		self.items = items
		self.textvariable = textvariable

		values = [i[0] for i in items]

		super().__init__(parent, textvariable, values[2], *values, command = lambda item=None: print(item), **kwargs)
#		self.configure(command = lambda : print(self.current()))
		self.bind('<<OptionMenuSelected>>', lambda item: self.textvariable.set(self.items[item][0]))


if __name__ == '__main__':
	import tkform

	form = tkform.TKForm('Micro Web Server')

	project = tkinter.StringVar(form)
	path = tkinter.StringVar(form)
	host = tkinter.StringVar(form)
	port = tkinter.StringVar(form)

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
	ttk.Style().configure('TLabel', foreground="#666666", font=labelFont)
	ttk.Style().configure('heading.TLabel', foreground='#133796', font=headingFont)
	ttk.Style().configure('link.TLabel', foreground='#133796', font=linkFont)
	ttk.Style().configure('link.hover.TLabel', foreground='#133796', font=linkHoverFont)
	ttk.Style().configure('TListbox', weight='normal', font=comboboxFont)
	form.option_add('*TCombobox*Listbox.font', comboboxFont)  # apply font to combobox list

	import sys
	if sys.platform == 'darwin': ttk.Style().configure('active.TButton', foreground='white')

	layout = {
		'Server': [
			[tkform.BoldLabel(form, text='Micro Web Server', foreground='#133796', font=headingFont), True, True, True, True],
			['Projects', True,  None, None, None],
			[
				tkform.Combobox(form, items=(('apple', 'a'), ('banana', 'b'), ('cherry', 'c'), ), textvariable=project, default='banana'), True,
				tkform.Button(form, 'Save', command=lambda *args: print('Save')),
				tkform.Button(form, 'Save As …', command=lambda *args: print('Save As …')),
				tkform.Button(form, 'Delete …', command=lambda *args: print('Delete …'))
			],
			['Path', True, True, True, None],
			[tkform.Textbox(form, font=entryFont, textvariable=path), True, True, True, tkform.Button(form, 'Select …', command=lambda *args: print('Select …')) ],
			['Host', True, True, 'Port', None],
			[
				tkform.Textbox(form, font=entryFont,  textvariable=host), True,
				tkform.Textbox(form, font=entryFont, textvariable=port), True,
				tkform.OKButton(form, 'Start', command=lambda *args: print('Start'))
			]
		],
		'About': [
			[tkform.BoldLabel(form, text='About Micro Web Server', foreground='#133796', font=headingFont), True, True, True, True],
			['© Mark Simon', True, True, True, True],
			[tkform.LinkLabel(form, text="https://github.com/manngo/micro-web-server/", style='link.TLabel'), True, True, True, True],
		]
	}
	form.doLayout(layout)
	# form.add(tkform.Label(form, text='Name'), row=1, column=1)
	# form.add(tkform.Textbox(form, textvariable=name, text='Fred'), row=1, column=2, columnspan=2)

	form.show()

	title = 'hello'
