#!/usr/bin/env python
# Scroll
# Developed by acidvegas in Python 3
# https://github.com/acidvegas/scroll
# scroll.py

import os
import sys

sys.dont_write_bytecode = True
os.chdir(sys.path[0] or '.')
sys.path += ('core',)

import debug
from database import Database

debug.info()
if not debug.check_version(3):
    debug.error_exit('Scroll requires Python 3!')
if debug.check_privileges():
    debug.error_exit('Do not run Scroll as admin/root!')
if not Database.check():
    Database.create()
import irc
irc.Scroll.connect()