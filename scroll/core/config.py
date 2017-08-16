#!/usr/bin/env python
# Scroll
# Developed by acidvegas in Python
# https://github.com/acidvegas/scroll
# config.py

class connection:
	server     = 'irc.server.com'
	port       = 6667
	proxy      = None
	ipv6       = False
	ssl        = False
	ssl_verify = False
	vhost      = None
	channel    = '#chat'
	key        = None

class cert:
	key      = None
	file     = None
	password = None

class ident:
	nickname = 'scroll'
	username = 'scroll'
	realname = 'ASCII Art Bot'

class login:
	network  = None
	nickserv = None
	operator = None

class settings:
	admin = 'change.me'
	cmd_char = '.'
	log   = False
	modes = None