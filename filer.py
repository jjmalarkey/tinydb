#!/usr/bin/env python3

import os, json, sys

class Filer:
	def __init__(self, db):
		self.root = db
		print(db)
	def create_file(self, filename, data):
		print(filename)
		if(os.path.exists(filename)):
			raise ValueError("Cannot create file: file already exists")
		with open(self.root + '/' + filename, "w") as wr:
			json.dump(data, wr)
			wr.close()
	def read_file(self, filename):
		try:
			rd = open(self.root + '/' + filename, "r")
			return json.load(rd)
		except FileNotFoundError:
			print("exception caugh")
			raise FileNotFoundError("cannot load data")
	def update_file(self, filename, data):
		try:
			wr = open(self.root + '/' + filename, "w")
			json.dump(data, wr)
			wr.close()
		except FileNotFoundError:
			raise FileNotFoundError("cannot update data")
	def delete_file(self, filename):
		try:
			os.remove(self.root + '/' + filename)
		except FileNotFoundError:
			raise ValueError("cannot delete data")
