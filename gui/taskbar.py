import win32api, win32con, win32gui
# from collections import OrderedDict
def MessageBox(title, text, style=1):
	##  Styles:
	##  0 : OK
	##  1 : OK | Cancel
	##  2 : Abort | Retry | Ignore
	##  3 : Yes | No | Cancel
	##  4 : Yes | No
	##  5 : Retry | No 
	##  6 : Cancel | Try Again | Continue
	##  Codes:
	## IDOK			: 1 The OK button was selected.
	## IDCANCEL		: 2 The Cancel button was selected.
	## IDABORT		: 3 The Abort button was selected.
	## IDRETRY		: 4 The Retry button was selected.
	## IDIGNORE		: 5 The Ignore button was selected.
	## IDYES		: 6
	## IDNO			: 7 The No button was selected.
	## IDTRYAGAIN	: 10 The Try Again button was selected.
	## IDCONTINUE	: 11 The Continue button was selected.
	results = win32api.MessageBox(None,text, title, style)
	return results

class TrayIcon:
	def __init__(self):
		self.visible=0
		self.events = {
			win32con.WM_DESTROY	: self.onDestroy,
			win32con.WM_USER+20	: self.onTaskbarNotify,
			win32con.WM_COMMAND	: self.onCommand
			# win32con.WM_USER+5	: self.onBalloonClick
		}
		self.windowtext = "window text"
		self.windowclassname = "window class name"

		window = win32gui.WNDCLASS()
		self.handlerInstance = window.hInstance = win32api.GetModuleHandle(None)
		window.lpszClassName = self.windowclassname
		window.style = win32con.CS_VREDRAW | win32con.CS_HREDRAW
		window.hCursor = win32gui.LoadCursor( 0, win32con.IDC_ARROW )
		window.hbrBackground = win32con.COLOR_WINDOW
		window.lpfnWndProc = self.events

		classAtom = win32gui.RegisterClass(window)
		style = win32con.WS_OVERLAPPED | win32con.WS_SYSMENU
		self.hwnd = win32gui.CreateWindow( classAtom, self.windowtext, style, 0, 0, win32con.CW_USEDEFAULT, win32con.CW_USEDEFAULT, 0, 0, self.handlerInstance, None)
		win32gui.UpdateWindow(self.hwnd)
		self.setIcon()

	def show(self):
		flags = win32gui.NIF_ICON | win32gui.NIF_MESSAGE
		if self.tooltip is not None:
			flags |= win32gui.NIF_TIP
			nid = (self.hwnd, 0, flags, win32con.WM_USER+20, self.icon, self.tooltip)#
		else:
			nid = (self.hwnd, 0, flags, win32con.WM_USER+20, self.icon)
		if self.visible:
			self.hide()
		win32gui.Shell_NotifyIcon(win32gui.NIM_ADD, nid)
		self.visible = 1
	def hide(self):
		if self.visible:
			nid = (self.hwnd, 0)
			win32gui.Shell_NotifyIcon(win32gui.NIM_DELETE, nid)
		self.visible = 0
	def setIcon(self, hicon=None, tooltip=None):
		if type(hicon) == str:
			icon_flags = win32con.LR_LOADFROMFILE | win32con.LR_DEFAULTSIZE
			try:
				# hicon = win32gui.LoadImage(self.handlerInstance, hicon, win32con.IMAGE_ICON, 0, 0, icon_flags)
				hicon = win32gui.LoadImage(0, hicon, win32con.IMAGE_ICON, 0, 0, win32con.LR_LOADFROMFILE)

			except Exception, e:
				hicon = win32gui.LoadIcon(0, win32con.IDI_APPLICATION)
		elif hicon == None:
			hicon = win32gui.LoadIcon(0, win32con.IDI_APPLICATION)
		self.icon = hicon
		self.tooltip = tooltip
	def Run(self):
		win32gui.PumpMessages()
		pass
	def End(self):
		self.hide()
		win32gui.PostQuitMessage(0) # Terminate the app.
	def onDestroy(self):
		self.hide()
		win32gui.PostQuitMessage(0) # Terminate the app.
	def notify(self, title="", message="", tiptext="", timeout=1, infoflags = win32gui.NIIF_INFO):
		flags = win32gui.NIF_ICON | win32gui.NIF_MESSAGE | win32gui.NIF_INFO
		nid = (self.hwnd, 0, flags, win32con.WM_USER+20, self.icon, tiptext, message, (10 * timeout), title, infoflags)
		win32gui.Shell_NotifyIcon(win32gui.NIM_MODIFY, nid)
	def createMenu(self, items):
		self.menu = win32gui.CreatePopupMenu()
		self.menuitems =[]
		for index, (key, value) in enumerate(items):
		# for index, key in enumerate(items):
		# for index, item in items :
			# key = items[index][0], value = items[index][1]
			self.menuitems.append(key)
			win32gui.AppendMenu(self.menu, win32con.MF_STRING, (1023 + index), value )
		# for index, title in enumerate(items):
		# 	AppendMenu(self.menu, win32con.MF_STRING, (1023 + index), title)
	def onTaskbarNotify(self, hwnd, msg, wparam, lparam):
		if lparam == win32con.WM_USER+5:
			self.onBalloonClick(hwnd, msg, wparam, lparam)
		elif lparam == win32con.WM_LBUTTONUP:
			self.onClick(hwnd, msg, wparam, lparam)
		elif lparam == win32con.WM_LBUTTONDBLCLK:
			self.onDoubleClick(hwnd, msg, wparam, lparam)
		elif lparam == win32con.WM_RBUTTONUP:
			if len(self.menuitems) > 0 and self.menu:
				x, y = win32api.GetCursorPos()
				win32gui.SetForegroundWindow(hwnd)
				win32gui.TrackPopupMenu(self.menu, win32con.TPM_LEFTALIGN, x, y, 0, hwnd, None)
				win32gui.PostMessage(hwnd, win32con.WM_NULL, 0, 0)
			# self.onRightClick(hwnd, msg, wparam, lparam)

		return 1
	def onCommand(self, hwnd, msg, wparam, lparam):
		id = wparam - 1023
		method = self.menuitems[id]
		if hasattr(self,method) and callable(getattr(self,method)):
			getattr(self, method)()
		# else:
		# 	print "Undefined method for " + method


		# self.menuitems[]
		# if callable(getattr(self, method))
		# 	getattr(self, method)
		# pass
	def onClick(self, hwnd, msg, wparam, lparam):
		pass
	def onDoubleClick(self, hwnd, msg, wparam, lparam):
		pass
	def onRightClick(self, hwnd, msg, wparam, lparam):
		pass
	def onBalloonClick(self, hwnd, msg, wparam, lparam):
		pass
