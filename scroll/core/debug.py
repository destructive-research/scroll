#!/usr/bin/env python
# Scroll
# Developed by acidvegas in Python
# https://github.com/acidvegas/scroll
# debug.py

import ctypes
import logging
import os
import sys
import time

from logging.handlers import RotatingFileHandler

import config

def check_privileges():
	if check_windows():
		if ctypes.windll.shell32.IsUserAnAdmin() != 0:
			return True
		else:
			return False
	else:
		if os.getuid() == 0 or os.geteuid() == 0:
			return True
		else:
			return False

def check_version(major):
	if sys.version_info.major == major:
		return True
	else:
		return False

def check_windows():
	if os.name == 'nt':
		return True
	else:
		return False

def clear():
	if check_windows():
		os.system('cls')
	else:
		os.system('clear')

def error(msg, reason=None):
	if reason:
		logging.error(f'[!] - {msg} ({reason})')
	else:
		logging.error('[!] - ' + msg)

def error_exit(msg):
	raise SystemExit('[!] - ' + msg)

def info():
	clear()
	print('#'*56)
	print('#{0}#'.format(''.center(54)))
	print('#{0}#'.format('Scroll'.center(54)))
	print('#{0}#'.format('Developed by acidvegas in Python'.center(54)))
	print('#{0}#'.format('https://github.com/acidvegas/scroll'.center(54)))
	print('#{0}#'.format(''.center(54)))
	print('#'*56)

def irc(msg):
	logging.debug('[~] - ' + msg)

def setup_logger():
	stream_handler = logging.StreamHandler(sys.stdout)
	if config.settings.log:
		log_file     = os.path.join(os.path.join('data','logs'), 'scroll.log')
		file_handler = RotatingFileHandler(log_file, maxBytes=256000, backupCount=3)
		logging.basicConfig(level=logging.NOTSET, format='%(asctime)s | %(message)s', datefmt='%I:%M:%S', handlers=(file_handler,stream_handler))
	else:
		logging.basicConfig(level=logging.NOTSET, format='%(asctime)s | %(message)s', datefmt='%I:%M:%S', handlers=(stream_handler,))
