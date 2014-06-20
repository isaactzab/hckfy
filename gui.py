import os, sys, threading, time, json
from gui.taskbar import *
from lib.audio_win import *
from lib.spotify_win import *
from lib.spotify_remote import *

class trayicon(TrayIcon):
	def __init__(self):
		TrayIcon.__init__(self)
		iconpath = os.path.abspath( "icon.ico" );
		self.setIcon(iconpath)
		self.show()
		self.fnOnBalloonClick = None
	def about(self):
		print "about"
	def donate(self):
		print "donate"
	def updatedb(self):
		print "updatedb"
	def reportad(self):
		self.notify("The balloons - Song of ads - Click me!", "Click here if this is an Ad!")
	def thisisnotad(self):
		print "thisisnotad"
	def exit(self):
		if MessageBox('Exit', 'Do you want to exit?', 4 ) == 6:
			self.End()
		# self.End()
	def onBalloonClick(self, hwnd, msg, wparam, lparam):
		if self.fnOnBalloonClick != None:
			self.fnOnBalloonClick()
		# MessageBox('Report as Ad', 'Do you want report this as Ad?', 4 )
	def setOnBaloonClick(self, fn):
		self.fnOnBalloonClick = fn


class Spotify(spotify_win):
	def __init__(self, sponsors):
		spotify_win.__init__(self, sponsors)
		self.callback = None
		self.interval = 1
		self.audio = Audio()
		self.remote = spotify_remote()
		self.laststatus = None

	def onSongChange(self, callback):
		self.callback = callback

	def Run(self):
		while True:
			status = self.status()
			compare = status == self.laststatus
			self.laststatus = status
			lastaudiostatus = True
			# print compare
			# print status
			if compare == False:
				print status
				self.callback(status)
				if(status["app"] != None) and (status["nowplaying"] != None and status["nowplaying"]["sponsor"] != None):
					self.audio.SetMute(True)
					self.remote.unpause()
					lastaudiostatus = False
				elif lastaudiostatus == False:
					self.audio.SetMute(False)
					lastaudiostatus = True
				
			# if self.current == 5 and self.callback is not None:
			# 	self.callback(self.current)
			# 	self.current =0
			time.sleep(self.interval)

class Sponsors:
	def __init__(self):
		self.path = os.path.abspath("sponsors.json")
		self.load()
		pass
	def load(self):
		if(os.path.isfile(self.path)):
			self.sponsors = json.load(open(self.path))
		else:
			self.sponsors = []
	def pull(self, path):
		pass
	def push(self, path):
		pass
	def get(self):
		return self.sponsors
	def append(self, object):
		self.sponsors.append(object)
	def save(self):
		with open(self.path, "w") as jsonfile:
			jsonfile.write(vars(self.sponsors))

class Application:
	def __init__(self):
		self.tray = trayicon()
		self.sponsors = Sponsors()
		self.spotify = Spotify(self.sponsors.get())
		self.spotify_daemon = None
		self.lastspoti = None

		self.tray.setOnBaloonClick(self.onBalloonClick)
				
		self.spotify.onSongChange(self.spotify_onSongChange)
		self.spotify_daemon = threading.Thread(target = self.spotify.Run, name = "spotify_daemon")
		self.spotify_daemon.setDaemon(True)
		#
		self.tray.createMenu([
			("about", "About"),
			("donate", "Donate now"),
			("updatedb", "Update database"),
			("reportad", "This is an ad"),
			("thisisnotad", "This is not ad"),
			("exit", "&Exit")
		])
		self.spotify_daemon.start()
		self.tray.Run()
	def spotify_onSongChange(self, spoti):
		if spoti['status'] == True:
			self.tray.notify( spoti['nowplaying']['artist'] + " - " +spoti['nowplaying']['artist'], "If this an ad click here")
			self.lastspoti = spoti
	def onBalloonClick(self):
		if MessageBox('Sponsor reporter', 'Do you want report as sponsor?', 4 ) == 6:
			self.sponsors.append(self.lastspoti)
			self.sponsors.save()

			



if __name__=='__main__':
	App = Application()
	# cig0-0019c72bbbd0