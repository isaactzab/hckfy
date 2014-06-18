import win32api, win32con, win32gui
from gui.taskbar import TrayIcon

if __name__=='__main__':
	class trayicon(TrayIcon):
		def __init__(self):
			TrayIcon.__init__(self)
			self.setIcon(win32gui.LoadIcon(0, win32con.IDI_APPLICATION))
			self.show()
		def onClick(self, hwnd, msg, wparam, lparam):
			self.notify('Tooltip title', 'Message')
			print "clicked"
		def onDoubleClick(self, hwnd, msg, wparam, lparam):
			print "bye bye..."
			win32gui.PostQuitMessage(0)
		

	tray = trayicon()
	win32gui.PumpMessages()