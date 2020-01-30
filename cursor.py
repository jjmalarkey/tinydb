#!/usr/bin/env python3

import os, json, sys

import filer, parser

class Cursor:
	def _load(self, db):
		if not(os.path.exists(db) and os.path.isdir(db)):
			#create the directory for the database first
			try:
				os.mkdir(db)
			except OSError:
				raise OSError("Initialization of db {} failed", db)
			print("Initialization of db {} succeeded", db)
#		os.chdir(db)
		self.root = db
		self.subsets = [file for file in os.listdir(self.root) if os.path.isdir(file)]
		self.subfiles = [file for file in os.listdir(self.root) if os.path.isfile(file)]
		self.nodedata = {}
		self.cFiler = filer.Filer(db)
		try:
			self.nodedata = self.cFiler.read_file('.tinydat.json')
		except IOError:
			self.cFiler.create_file('.tinydat.json', self.nodedata)
		self.cParser = parser.Parser(db)
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
	def leaf(self, leaf):
		if leaf not in self.subfiles:
			cFiler.create_file(leaf, [])
			print("leaf {} created ({})".format(leaf, self.root))
		self._load(self.root)
		return parser.Parser(self.root, leaf)
