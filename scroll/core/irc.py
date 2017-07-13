#!/usr/bin/env python
# Scroll
# Developed by acidvegas in Python 3
# https://github.com/acidvegas/scroll
# irc.py

import glob
import inspect
import os
import random
import socket
import ssl
import threading
import time

import config
import debug
import functions
from database import Ignore, Settings

# Globals
ascii_dir = os.path.join('data', 'ascii')

# Formatting Control Characters / Color Codes
bold        = '\x02'
italic      = '\x1D'
underline   = '\x1F'
reverse     = '\x16'
reset       = '\x0f'
white       = '00'
black       = '01'
blue        = '02'
green       = '03'
red         = '04'
brown       = '05'
purple      = '06'
orange      = '07'
yellow      = '08'
light_green = '09'
cyan        = '10'
light_cyan  = '11'
light_blue  = '12'
pink        = '13'
grey        = '14'
light_grey  = '15'

class IRC(object):
	def __init__(self):
		self.auto    = False
		self.last    = 0
		self.playing = False
		self.slow    = False
		self.stopper = False
		self.sock    = None

	def color(self, msg, foreground, background=None):
		if background:
			return f'\x03{foreground},{background}{msg}{reset}'
		else:
			return f'\x03{foreground}{msg}{reset}'

	def connect(self):
		try:
			self.create_socket()
			self.sock.connect((config.connection.server, config.connection.port))
			self.register()
		except socket.error as ex:
			debug.error('Failed to connect to IRC server.', ex)
			self.event_disconnect()
		else:
			self.listen()

	def create_socket(self):
		family	= socket.AF_INET6 if config.connection.ipv6 else socket.AF_INET
		self.sock = socket.socket(family, socket.SOCK_STREAM)
		if config.connection.vhost:
			self.sock.bind((config.connection.vhost, 0))
		if config.connection.ssl:
			self.sock = ssl.wrap_socket(self.sock, keyfile=config.ssl.key, certfile=config.ssl.file)

	def error(self, chan, msg, reason=None):
		if reason:
			self.sendmsg(chan, '[{0}] {1} {2}'.format(self.color('ERROR', red), msg, self.color(f'({reason})', grey)))
		else:
			self.sendmsg(chan, '[{0}] {1}'.format(self.color('ERROR', red), msg))

	def event_connect(self):
		if config.settings.user_modes:
			self.mode(config.ident.nickname, '+' + config.settings.user_modes)
		if config.login.nickserv:
			self.identify(config.ident.nickname, config.login.nickserv)
		if config.login.operator:
			self.oper(config.ident.username, config.login.operator)
		self.join_channel(config.connection.channel, config.connection.key)
		self.join_channel('#scroll')

	def event_disconnect(self):
		self.sock.close()
		time.sleep(10)
		self.connect()

	def event_kick(self, nick, chan, kicked):
		if kicked == config.ident.nickname:
			if chan == config.connection.channel:
				time.sleep(3)
				self.join_channel(chan, config.connection.key)
			elif chan == '#scroll':
				time.sleep(3)
				self.join_channel(chan)

	def event_message(self, nick, host, chan, msg):
		if chan == config.connection.channel or chan == '#scroll':
			args = msg.split()
			if args[0] == '.ascii' and host not in Ignore.hosts():
				if time.time() - self.last < Settings.get('cmd_throttle') and host != config.settings.admin_host:
					if not self.slow:
						self.error(chan, 'Slow down nerd!')
						self.slow = True
				else:
					self.slow = False
					if self.playing or self.auto:
						if msg == '.ascii stop':
							if self.auto:
								self.auto = False
							if not self.stopper:
								self.stopper = True
						else:
							self.error(chan, 'Please wait for the current ASCII to finish playing!')
					elif len(args) == 2:
						option = args[1]
						if option == 'auto' and host == config.settings.admin_host and not self.auto:
							threading.Thread(target=self.auto, args=(chan,)).start()
						else:
							if option == 'random':
								ascii_file = random.choice(glob.glob(os.path.join(ascii_dir, '**/*.txt'), recursive=True))
							else:
								ascii_file = (glob.glob(os.path.join(ascii_dir, f'**/{option}.txt'), recursive=True)[:1] or [None])[0]
							if ascii_file:
								data  = open(ascii_file, encoding='utf8', errors='replace').read()
								if len(data.splitlines()) > Settings.get('max_lines') and chan != '#scroll':
									self.error(chan, 'File is too big.', 'Take it to #scroll')
								else:
									if args[1] == 'random':
										self.sendmsg(chan, os.path.basename(ascii_file))
									threading.Thread(target=self.play, args=(chan, data)).start()
							else:
								self.error(chan, 'Invalid file name.', 'Use ".ascii list" for a list of valid file names.')
					elif len(args) == 3:
						if args[1] == 'search':
							query	   = args[2]
							ascii_files = glob.glob(os.path.join(ascii_dir, f'**/*{query}*.txt'), recursive=True)
							if ascii_files:
								ascii_files = ascii_files[:Settings.get('max_results')]
								for file_name in ascii_files:
									count = ascii_files.index(file_name) + 1
									self.sendmsg(chan, '{0} {1}'.format(self.color('[{0}]'.format(count), pink), os.path.basename(file_name)))
							else:
								self.error(chan, 'No results found.')
				self.last = time.time()

	def event_private(self, nick, host, msg):
		if host == config.settings.admin_host:
			args = msg.split()
			if len(args) == 1:
				if msg == '.config':
					settings = Settings.read()
					self.sendmsg(nick, '[{0}]'.format(self.color('Settings', purple)))
					for setting in settings:
						self.sendmsg(nick, '{0} = {1}'.format(self.color(setting[0], yellow), self.color(setting[1], grey)))
				elif msg == '.ignore':
					ignores = Ignore.read()
					if ignores:
						self.sendmsg(nick, '[{0}]'.format(self.color('Ignore List', purple)))
						for user in ignores:
							self.sendmsg(nick, '{0} {1}'.format(self.color(user[0], yellow), self.color(f'({user[1]})', grey)))
						self.sendmsg(nick, '{0} {1}'.format(self.color('Total:', light_blue), self.color(len(ignores), grey)))
					else:
						self.error(nick, 'Ignore list is empty!')
				elif msg == '.off':
					self.auto    = False
					self.stopper = True
					self.sendmsg(nick, self.color('OFF', red))
					self.part(self.channel, 'Bot has been turned off.')
				elif msg == '.on':
					self.stopper = False
					self.sendmsg(nick, self.color('ON', green))
					self.join_channel(config.connection.channel, config.connection.key)
			elif len(args) == 3:
				if args[0] == '.config':
					setting, value = args[1], args[2]
					if functions.CheckString.number(value):
						value = functions.floatint(value)
						if value >= 0:
							if setting in Settings.settings():
								Settings.update(setting, value)
								self.sendmsg(nick, 'Change setting for {0} to {1}.'.format(self.color(setting, yellow), self.color(value, grey)))
							else:
								self.error(nick, 'Invalid config variable.')
						else:
							self.error(nick, 'Value must be greater than or equal to zero.')
					else:
						self.error(nick, 'Value must be an integer or float.')
			elif len(args) == 4:
				if args[0] == '.ignore':
					if args[1] == 'add':
						nickname, hostname = args[2], args[3]
						if hostname != config.settings.admin_host:
							if len(nickname) <= 20 and len(hostname) <= 63:
								if functions.CheckString.hostname(hostname) and functions.CheckString.nickname(nickname):
									if hostname not in Ignore.hosts():
										Ignore.add(nickname, hostname)
										self.sendmsg(nick, 'User {0} to the ignore list.'.format(self.color('added', green)))
									else:
										self.error(nick, 'Host is already on the ignore list.')
								else:
									self.error(nick, 'Nick/Host contains illegal characters.')
							else:
								self.error(nick, 'Nick/Host is too long.')
						else:
							self.error(nick, 'Admin host can not be ignored.')
					elif args[1] == 'del':
						nickname, hostname = args[2], args[3]
						if hostname in Ignore.hosts():
							Ignore.remove(nickname, hostname)
							self.sendmsg(nick, 'User {0} from the ignore list.'.format(self.color('removed', red)))
						else:
							self.error(nick, 'User does not exist in the ignore list.')

	def event_nick_in_use(self):
		debug.error_exit('Scroll is already running.')

	def handle_events(self, data):
		args = data.split()
		if data.startswith('ERROR :Closing Link:'):
			raise Exception('Connection has closed.')
		if args[0] == 'PING':
			self.raw('PONG ' + args[1][1:])
		elif args[1] == '001':
			self.event_connect()
		elif args[1] == '433':
			self.event_nick_in_use()
		elif args[1] == 'KICK':
			nick   = args[0].split('!')[0][1:]
			chan   = args[2]
			kicked = args[3]
			self.event_kick(nick, chan, kicked)
		elif args[1] == 'PRIVMSG':
			nick = args[0].split('!')[0][1:]
			host = args[0].split('!')[1].split('@')[1]
			chan = args[2]
			msg  = data.split(f'{args[0]} PRIVMSG {chan} :')[1]
			if chan == config.ident.nickname:
				self.event_private(nick, host, msg)
			else:
				self.event_message(nick, host, chan, msg)

	def identify(self, nick, passwd):
		self.sendmsg('nickserv', f'recover {nick} {passwd}')
		self.sendmsg('nickserv', f'identify {nick} {passwd}')

	def join_channel(self, chan, key=None):
		if key:
			self.raw(f'JOIN {chan} {key}')
		else:
			self.raw('JOIN ' + chan)

	def listen(self):
		while True:
			try:
				data = self.sock.recv(1024).decode('utf-8')
				for line in [line for line in data.split('\r\n') if line]:
					debug.irc(line)
					if len(line.split()) >= 2:
						self.handle_events(line)
			except (UnicodeDecodeError,UnicodeEncodeError):
				pass
			except Exception as ex:
				debug.error('Unexpected error occured.', ex)
				break
		self.event_disconnect()

	def mode(self, target, mode):
		self.raw(f'MODE {target} {mode}')

	def oper(self, user, passwd):
		self.raw(f'OPER {user} {passwd}')

	def part(self, chan, msg=None):
		if msg:
			self.raw(f'PART {chan} {msg}')
		else:
			self.raw('PART ' + chan)

	def auto(self, chan, files=None):
		self.auto = True
		while True:
			if not self.auto:
				break
			try:
				ascii_file = random.choice(glob.glob(os.path.join(ascii_dir, '**/*.txt'), recursive=True))
				data       = open(ascii_file, encoding='utf8', errors='replace').read()
				self.sendmsg(chan, os.path.basename(ascii_file))
				threading.Thread(target=self.play, args=(chan, data)).start()
			except Exception as ex:
				debug.error('Error occured in the auto function!', ex)
				break
			else:
				time.sleep(Settings.get('cmd_throttle'))
				while self.playing:
					time.sleep(1)
		self.auto = False

	def play(self, chan, data):
		self.playing = True
		for line in [line for line in data.splitlines() if line]:
			if self.stopper:
				break
			try:
				self.sendmsg(chan, line[:400])
			except Exception as ex:
				debug.error('Error occured in the play function!', ex)
				break
			else:
				time.sleep(Settings.get('msg_throttle'))
		self.stopper = False
		self.playing = False

	def raw(self, msg):
		self.sock.send(bytes(msg + '\r\n', 'utf-8'))

	def register(self):
		if config.login.network:
			self.raw('PASS ' + config.login.network)
		self.raw(f'USER {config.ident.username} 0 * :{config.ident.realname}')
		self.raw('NICK '+ config.ident.nickname)

	def sendmsg(self, target, msg):
		self.raw(f'PRIVMSG {target} :{msg}')

Scroll = IRC()