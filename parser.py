#!/usr/bin/env python3

import os, json, sys

import filer

class Parser:
	def __init__(self, db, file=None):
		self.root = db
		self.pFiler = filer.Filer(db)
		if file is not None:
			self.file = file
			self.data = self.pFiler.read_file(file)
	def load_data(self, file):
		self.file = file
		self.data = self.pFiler.read_file(file)
	def find(self, **kwargs):
		parsingdata = self.data
		def _match(tEntry):
			criteriamatch = True
			for field, match in kwargs.items():
				if isinstance(match, list):
					try:
						if field not in tEntry or not all(x in tEntry[field] for x in match):
							criteriamatch = False
							break
					except TypeError:
						print('{}: not a set model for match inclusive.'.format(field))
						break
				else:
					if field not in tEntry or tEntry[field] != match:
						criteriamatch = False
						break
			return criteriamatch
		def _find_hash():
			results = []
			for key, entry in parsingdata.items():
				if _match(entry):
					entry["keyid"] = key
					results.append(entry)
			return results
		def _find_arr():
			results = []
			for entry in parsingdata:
				if _match(entry):
					results.append(entry)
			return results
		if isinstance(self.data, dict):
			self.results = _find_hash()
		elif isinstance(self.data, list):
			self.results = _find_arr()
	def export(self):
		return self.results
	def update(self, critdict, **kwargs):
		parsingdata = self.data
		if not dict:
			raise ValueError("Require at least one criteria for updating data")
		def _match(tEntry):
			criteriamatch = True
			for f, m in critdict.items():
				if isinstance(m, list):
					try:
						if field not in tEntry or not all(x in tEntry[f] for x in m):
							criteriamatch = False
							break
					except TypeError:
						print('{}: not a set model for match inclusive.'.format(field))
						break
				else:
					if f not in tEntry or tEntry[f] != m:
						criteriamatch = False
						break
			return criteriamatch
		def _update_hash():
			count = 0
			for k, v in parsingdata.items():
				if _match(v):
					count = count+1
					for field, value in kwargs.items():
						parsingdata[k][field] = value
		def _update_arr():
			count = 0
			for i in range(len(parsingdata)):
				v = parsingdata[i]
				if _match(v):
					count = count+1
					for field, value in kwargs.items():
						v[field] = value
					parsingdata[i] = v
		number_changed = 0
		if isinstance(self.data, dict):
			number_changed = _update_hash()
		elif isinstance(self.data, list):
			number_changed = _update_arr()
		return number_changed
	def insert(self, data, key=None):
		parsingdata = self.data
		if isinstance(self.data, dict):
			if key is None:
				raise ValueError("{} is a key driven table, and a key is needed to insert".format(self.file))
			else:
				parsingdata[key] = data
		elif isinstance(self.data, list):
			parsingdata.append(data)
	def commit_data(self, file):
		self.pFiler.update_file(file, self.data)
