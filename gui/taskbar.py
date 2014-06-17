import win32api, win32con, win32gui
class Taskbar{
	def __init__(self):
		self.visible=0
		self.events = {
			win32con.WM_DESTROY	: self.onDestroy,
			win32con.WM_USER+20	: self.onTaskbarNotify
			# win32con.WM_USER+5	: self.onBalloonClick
		}
		self.windowtext = "window text"
		self.windowclassname = "window class name"

		window = win32gui.WNDCLASS()
		handlerInstance = window.hInstance = win32api.GetModuleHandle(None)
		window.lpszClassName = self.windowclassname
		window.style = win32con.CS_VREDRAW | win32con.CS_HREDRAW
		window.hCursor = win32gui.LoadCursor( 0, win32con.IDC_ARROW )
		window.hbrBackground = win32con.COLOR_WINDOW
		window.lpfnWndProc = self.events

		classAtom = win32gui.RegisterClass(window)
		style = win32con.WS_OVERLAPPED | win32con.WS_SYSMENU
		self.hwnd = win32gui.CreateWindow( classAtom, self.windowtext, style, 0, 0, win32con.CW_USEDEFAULT, win32con.CW_USEDEFAULT, 0, 0, hinst, None)
		win32gui.UpdateWindow(self.hwnd)

	def show(self):
		flags = win32gui.NIF_ICON | win32gui.NIF_MESSAGE
		if self.tooltip is not None:
			flags |= win32gui.NIF_TIP
			nid = (self.hwnd, 0, flags, win32con.WM_USER+20, self.hicon, self.tooltip)#
		else:
			nid = (self.hwnd, 0, flags, win32con.WM_USER+20, self.hicon)
		if self.visible:
			self.hide()
		win32gui.Shell_NotifyIcon(win32gui.NIM_ADD, nid)
		self.visible = 1

	def hide(self):
		if self.visible:
			nid = (self.hwnd, 0)
			win32gui.Shell_NotifyIcon(win32gui.NIM_DELETE, nid)
		self.visible = 0

	def seticon(self, hicon, tooltip=none):
		self.icon = hicon
		self.tooltip = tooltip

	def onDestroy(self):
		self.hide()
		win32gui.PostQuitMessage(0) # Terminate the app.
	def onTaskbarNotify(self, hwnd, msg, wparam, lparam):




}