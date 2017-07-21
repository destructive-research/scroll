#!/usr/bin/env python
# Scroll
# Developed by acidvegas in Python 3
# https://github.com/acidvegas/scroll
# functions.py

import inspect
import os
import sqlite3

# Globals
db_file = os.path.join('data', 'scroll.db')
db      = sqlite3.connect(db_file, check_same_thread=False)
sql     = db.cursor()

def check():
	tables = sql.execute('SELECT name FROM sqlite_master WHERE type=\'table\'').fetchall()
	if not len(tables):
		sql.execute('CREATE TABLE IGNORE (NICK TEXT NOT NULL, HOST TEXT NOT NULL);')
		sql.execute('CREATE TABLE SETTINGS (SETTING TEXT NOT NULL, VALUE INTEGER NOT NULL);')
		sql.execute('INSERT INTO SETTINGS (SETTING,VALUE) VALUES (?, ?)', ('cmd_throttle', 3))
		sql.execute('INSERT INTO SETTINGS (SETTING,VALUE) VALUES (?, ?)', ('msg_throttle', 0.03))
		sql.execute('INSERT INTO SETTINGS (SETTING,VALUE) VALUES (?, ?)', ('max_lines', 50))
		sql.execute('INSERT INTO SETTINGS (SETTING,VALUE) VALUES (?, ?)', ('max_results', 10))
		db.commit()

class Ignore:
	def add(nick, host):
		sql.execute('INSERT INTO IGNORE (NICK,HOST) VALUES (?, ?)', (nick, host))
		db.commit()

	def hosts():
		return list(item[0] for item in sql.execute('SELECT HOST FROM IGNORE').fetchall())

	def read():
		return sql.execute('SELECT NICK,HOST FROM IGNORE ORDER BY NICK ASC, HOST ASC').fetchall()

	def remove(nick, host):
		sql.execute('DELETE FROM IGNORE WHERE NICK=? AND HOST=?', (nick, host))
		db.commit()



class Settings:
	def get(setting):
		return sql.execute('SELECT VALUE FROM SETTINGS WHERE SETTING=?', (setting,)).fetchone()[0]

	def read():
		return sql.execute('SELECT SETTING,VALUE FROM SETTINGS ORDER BY SETTING ASC').fetchall()

	def settings():
		return list(item[0] for item in sql.execute('SELECT SETTING FROM SETTINGS').fetchall())

	def update(setting, value):
		sql.execute('UPDATE SETTINGS SET VALUE=? WHERE SETTING=?', (value, setting))
		db.commit()