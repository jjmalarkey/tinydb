#!/usr/bin/env python3

import os, json, sys

import filer

class Parser:
	def __init__(self, db, file=None):
		self.root = db
		self.pFiler = filer.Filer(db)
		if file is not None:
			self.data = self.pFiler.read_file(file)
	def attach_data(self, file):
		self.data = self.pFiler.read_file(file)
	def find(self, **kwargs):
		parsingdata = self.data
		def _find_hash():
			results = []
			for key, entry in parsingdata.items():
				print(entry)
				criteriamatch = True
				for field, match in kwargs.items():
					print(field, match)
					print(entry[field])
					print(match)
					if field not in entry or entry[field] != match:
						criteriamatch = False
						break
				if criteriamatch:
					entry["keyid"] = key
					results.append(entry)
			return results
		def _find_arr():
			results = []
			for entry in parsingdata:
				criteriamatch = True
				for field, match in kwargs.items():
					if field not in entry or entry[field] != match:
						criteriamatch = False
						break
				if criteriamatch:
					results.append(entry)
			return results
		if isinstance(self.data, dict):
			self.results = _find_hash()
		elif isinstance(self.data, list):
			self.results = _find_arr()
