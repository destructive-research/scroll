#!/usr/bin/env python
# Scroll
# Developed by acidvegas in Python
# https://github.com/acidvegas/scroll
# functions.py

def check_int(data):
	if len(data) <= 4:
		if data.isdigit():
			return True
		elif data[:1].isdigit() and data.replace('.','',1).isdigit():
			return True
		else:
			return False
	else:
		return False

def floatint(data):
	if data.isdigit():
		return int(data)
	else:
		return float(data)