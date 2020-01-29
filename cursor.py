#!/usr/bin/env python3

import os, json, sys

class Cursor:
	def _load(self, db):
		if not(os.path.exists(db) and os.path.isdir(db)):
			#create the directory for the database first
			try:
				os.mkdir(path)
			except OSError:
				raise OSError("Initialization of db {} failed", db)
			else:
				print("Initialization of db {} succeeded", db)
		os.chdir(db)
		self.root = db
		self.subsets = [file for file in os.listdir(self.root) if os.path.isdir(file)]
		self.subfiles = [file for file in os.listdir(self.root) if os.path.isfile(file)]
		self.nodedata = {}
		try:
			with open(self.root + '/.tinydat.json', 'r') as rd:
				self.nodedata = json.load(rd)
				rd.close()
		except OSError:
			with open(self.root + '/.tinydat.json', 'w') as wr:
				json.dump({}, wr)
				wr.close()
	def __init__(self, db):
		self._load(db)
	def list_sets(self):
		return self.subsets
	def list_leaves(self):
		return self.subfiles
	def child(self, target):
		try:
			return Cursor(self.root + '/' + target)
		except OSError as e:
			raise OSError("Child spawn failed: " + e.message)
	def reload(self):
		self._load(self.root)
