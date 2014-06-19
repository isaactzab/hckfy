import os, sys
from gui.taskbar import *

if __name__=='__main__':
	class trayicon(TrayIcon):
		def __init__(self):
			TrayIcon.__init__(self)
			iconpath = os.path.abspath( "icon.ico" );
			self.setIcon(iconpath)
			self.show()
		# def onClick(self, hwnd, msg, wparam, lparam):
			

		def about(self):
			print "about"
		def donate(self):
			print "donate"
		def updatedb(self):
			print "updatedb"
		def reportad(self):
			print "reportad"
		def thisisnotad(self):
			print "thisisnotad"
		def exit(self):
			if MessageBox('Exit', 'Do you want to exit?', 4 ) == 6:
				self.End()

	tray = trayicon()
	tray.createMenu([
		("about", "About"),
		("donate", "Donate now"),
		("updatedb", "Update database"),
		("reportad", "This is an ad"),
		("thisisnotad", "This is not ad"),
		("exit", "&Exit")
	])
	tray.Run()
	