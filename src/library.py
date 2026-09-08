import sys, os
from pprint import pp, pformat

def dbug(data='', *args, pretty=False, **kwargs):
	fback = sys._getframe().f_back
	if pretty:
		data = pformat(data, sort_dicts=False)
	print(f'{os.path.basename(fback.f_code.co_filename)}:{fback.f_lineno}: ', data, *args, **kwargs)

import tkinter.messagebox
def say(message='Hello', title='Say'):
	fback = sys._getframe().f_back
	tkinter.messagebox.showinfo(title=title, message=f'{os.path.basename(fback.f_code.co_filename)}:{fback.f_lineno}: {message}')

class getset:
	def __init__(self, get=None, set=None):
		self.get = get
		self.set = set

	def __get__(self, instance, owner):
		return self.get(instance)
	def __set__(self, instance, value):
		self.set(instance, value)

	def setter(self, set):
		return getset(self.get, set)


