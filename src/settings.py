import os
import json
import re
from library import dbug
#from pprint import pp

class Settings:
	def __init__(self, filename, default={}, force=False):
		self.filename = filename
		self.dictionary = {}
		if force:
			os.unlink(self.filename)
		if os.path.isfile(self.filename) and not force:
			self.read()
		else:
		#	os.makedirs(os.path.dirname(f'./{self.filename}'), exist_ok=True)
			os.makedirs(os.path.dirname(self.filename), exist_ok=True)
			self.dictionary = default
			fh = open(self.filename, 'x')
			self.write()
			self.read()
			fh.close()

	def read(self):
		pass

	def write(self):
		pass

	def __setitem__(self, key, value):
		self.dictionary[key] = value
		self.write()

	def __getitem__(self, item):
		return self.dictionary[item] if item in self.dictionary else None

	def __iter__(self):
		return iter(self.dictionary)

	def __str__(self):
		return str(self.dictionary)

	def items(self):
		return self.dictionary.items()

	def keys(self):
		return self.dictionary.keys()

	def values(self):
		return self.dictionary.values()

	@property
	def data(self):
		return self.dictionary

	@data.setter
	def data(self, data):
		self.dictionary = data
		self.write()

	def retype(self, string, value=False):
		print(string)
		if re.match(r'[\'"](.*)\1', string):
			return string.strip('\'"') if value else str

		if string.lower() in ['true', 'false']:
			a = string.lower() == 'true'
			return a if value else bool


		try:
			a = int(string)
			return a if value else int
		except:
			try:
				a = float(string)
				return a if value else float
			except:
				return string if value else str

class IniSettings(Settings):
	def write(self):
		filehandle = open(self.filename, 'wt', encoding='utf-8')

		for k, v in self.dictionary.items():
			if isinstance(v, dict):
				filehandle.write(f'[{k}]\n')
				for k, v in v.items():
					filehandle.write(f'{k}={v}\n')
			else:
				filehandle.write(f'{k}={v}\n')

		filehandle.close()
		return self.dictionary

	def read(self):
		filehandle = open(self.filename, 'rt', encoding='utf-8')
		data = filehandle.readlines()
	#	data = filehandle.read().splitlines()
		filehandle.close()

		self.dictionary = {}
		section = self.dictionary
		regex = r'(\[(.*)\])|((.*?)=(.*))|(.*)'
		for item in data:
			item = item.strip();
			if not item: continue

			m = re.search(regex, item)
			print(m.group(4))
			if m.group(2):								#	[section]
				self.dictionary[m.group(2)] = {}
				section = self.dictionary[m.group(2)]
			elif m.group(4):							#	a=b
				value = m.group(5)
				section[m.group(4)] = self.retype(m.group(5), value=True)
			elif m.group(6):							#	boolean
				print(m.group(6))
				section[m.group(6)] = True

		return self.dictionary

class JSONSettings(Settings):
	def write(self):
		filehandle = open(self.filename, 'wt', encoding='utf-8')
		json.dump(self.dictionary, filehandle, indent='\t')
		filehandle.close()
		return self.dictionary

	def read(self):
		filehandle = open(self.filename, 'rt', encoding='utf-8')
		try:
			self.dictionary = json.load(filehandle)
		except Exception:
			pass
		filehandle.close()
		return self.dictionary
