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
	def reportsponsor(self):
		self.notify("The balloons - Song of ads - Click me!", "Click here if this is an Ad!")
	def exit(self):
		if MessageBox('Exit', 'Do you want to exit?', 4 ) == 6:
			self.End()
	def onBalloonClick(self, hwnd, msg, wparam, lparam):
		if self.fnOnBalloonClick != None:
			self.fnOnBalloonClick()
	def setOnBaloonClick(self, fn):
		self.fnOnBalloonClick = fn


class Spotify(spotify_win):
	def __init__(self, sponsors):
		self.sponsors = sponsors
		spotify_win.__init__(self)
		self.callback = None
		self.interval = 1
		self.audio = Audio()
		self.remote = spotify_remote()
		self.laststatus = None

	def onSongChange(self, callback):
		self.callback = callback
	def checkIfIsSponsor(self, currentsong):
		for sponsor in self.sponsors:
			if currentsong["artist"] == sponsor["artist"]:
				# TODO: Callback probable sponsor
				if currentsong["song"] == sponsor["song"]:
					return True
		return False
		# pass
	def Run(self):
		while True:
			status = self.status()
			compare = status == self.laststatus
			self.laststatus = status
			lastaudiostatus = True
			if compare == False and status["app"] != None and status["nowplaying"] != None and (status["nowplaying"]["artist"] != None and status["nowplaying"]["song"] != None):
				self.callback(status["nowplaying"])
				if self.checkIfIsSponsor(status["nowplaying"]):
					print "Blocking sponsor"
					self.audio.SetMute(True)
					self.remote.unpause()
					lastaudiostatus = False
				elif lastaudiostatus == False:
					print "Enabling audio"
					self.audio.SetMute(False)
					lastaudiostatus = True
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
			jsonfile.write(json.dumps(self.sponsors))

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
		self.tray.createMenu([
			("about", "About"),
			("reportsponsor", "Report it!"),
			("exit", "&Exit")
		])
		self.spotify_daemon.start()
		self.tray.Run()
	def spotify_onSongChange(self, spoti):
		# if spoti['status'] == True:
		print spoti
		self.tray.notify( spoti['artist'] + " - " +spoti['song'], "Click if this is a sponsor")
		self.lastspoti = spoti
	def onBalloonClick(self):
		if MessageBox('Sponsor reporter', 'Do you want report as sponsor?', 4 ) == 6:
			self.sponsors.append(self.lastspoti)
			self.sponsors.save()
if __name__=='__main__':
	App = Application()
# cig0-0019c72bbbd0