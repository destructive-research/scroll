#!/usr/bin/env python
# Scroll
# Developed by acidvegas in Python 3
# https://github.com/acidvegas/scroll
# functions.py

import string

class CheckString:
    def hostname(data):
		if len(data) <= 63:
	        chars = string.ascii_letters + string.digits + '-.:'
    	    return all(c in chars for c in data)
		else:
			return False

    def nickname(data):
		if len(data) <= 20:
	        chars = string.ascii_letters + string.digits + '`^-_[{]}|\\'
	        return all(c in chars for c in data)
		else:
			return False

    def number(data):
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