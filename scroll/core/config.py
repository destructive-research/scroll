#!/usr/bin/env python
# Scroll
# Developed by acidvegas in Python 3
# https://github.com/acidvegas/scroll
# config.py

class connection:
	server  = 'irc.server.com'
	port    = 6667
	ipv6    = False
	ssl     = False
	vhost   = None
	channel = '#chats'
	key     = None

class ident:
	nickname = 'scroll'
	username = 'scroll'
	realname = 'ASCII Art Bot'

class ssl:
	key  = None
	file = None

class login:
	network  = None
	nickserv = None
	operator = None

class settings:
	admin_host = 'admin.host'
	user_modes = None
