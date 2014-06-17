#!/usr/bin/python
# Based on win32gui_taskbar demo

#@PydevCodeAnalysisIgnore

from win32api import *
# Try and use XP features, so we get alpha-blending etc.
try:
	from winxpgui import *
except ImportError:
	from win32gui import *
import win32con
import sys, os
# from winswitch.util.simple_logger import Logger


class win32StatusIcon:
	def __init__(self, notify_callback, exit_callback, command_callback=None, iconPathName=None):
		# Logger(self)
		self.slog(None, notify_callback, exit_callback, command_callback, iconPathName)
		self.notify_callback = notify_callback
		self.exit_callback = exit_callback
		self.command_callback = command_callback
		message_map = {
			win32con.WM_DESTROY: self.OnDestroy,
			win32con.WM_COMMAND: self.OnCommand,
			win32con.WM_USER+20: self.OnTaskbarNotify,
		}
		# Register the Window class.
		wc = WNDCLASS()
		hinst = wc.hInstance = GetModuleHandle(None)
		wc.lpszClassName = "win32StatusIcon"
		wc.lpfnWndProc = message_map # could also specify a wndproc.
		classAtom = RegisterClass(wc)
		# Create the Window.
		style = win32con.WS_OVERLAPPED | win32con.WS_SYSMENU
		self.hwnd = CreateWindow(classAtom, 'IrfanView'+" StatusIcon Window", style, \
		0, 0, win32con.CW_USEDEFAULT, win32con.CW_USEDEFAULT, \
		0, 0, hinst, None)
		UpdateWindow(self.hwnd)
		icon_flags = win32con.LR_LOADFROMFILE | win32con.LR_DEFAULTSIZE
		try:
			hicon = LoadImage(hinst, iconPathName, win32con.IMAGE_ICON, 0, 0, icon_flags)
		except Exception, e:
			self.serr("Failed to load icon!", e, notify_callback, exit_callback, command_callback, iconPathName)
			hicon = LoadIcon(0, win32con.IDI_APPLICATION)
		flags = NIF_ICON | NIF_MESSAGE | NIF_TIP
		nid = (self.hwnd, 0, flags, win32con.WM_USER+20, hicon, 'IrfanView')
		Shell_NotifyIcon(NIM_ADD, nid)
	
	def OnCommand(self, hwnd, msg, wparam, lparam):
		self.sdebug(None, hwnd, msg, wparam, lparam)
		id = LOWORD(wparam)
		if self.command_callback:
			self.command_callback(self.hwnd, id)
		
	def OnDestroy(self, hwnd, msg, wparam, lparam):
		self.sdebug(None, hwnd, msg, wparam, lparam)
		try:
			nid = (self.hwnd, 0)
			Shell_NotifyIcon(NIM_DELETE, nid)
			self.exit_callback()
		except Exception, e:
			self.serr(None, e, hwnd, msg, wparam, lparam, e)

	def OnTaskbarNotify(self, hwnd, msg, wparam, lparam):
		self.sverbose(None, hwnd, msg, wparam, lparam)
		if lparam==win32con.WM_LBUTTONUP or lparam==win32con.WM_RBUTTONUP:
			self.notify_callback(hwnd)
		return 1

	def set_visible(self, visible):
		pass	#not implemented on win32
	
	def get_geometry(self):
		return	self.do_get_geometry(self.hwnd)

	def do_get_geometry(self, hwnd):
		return	GetWindowRect(hwnd)
	
	def get_size(self):
		geom = self.get_geometry()
		if not geom:
			return	None
		(left, top, right, bottom) = geom
		self.sverbose(None, left, top, right, bottom)
		return	top - bottom

def notify_callback(hwnd):
	menu = CreatePopupMenu()
	AppendMenu( menu, win32con.MF_STRING, 1024, "Generate balloon")
	AppendMenu( menu, win32con.MF_STRING, 1025, "Exit")
	pos = GetCursorPos()
	SetForegroundWindow(hwnd)
	TrackPopupMenu(menu, win32con.TPM_LEFTALIGN, pos[0], pos[1], 0, hwnd, None)
	PostMessage(hwnd, win32con.WM_NULL, 0, 0)

def command_callback(hwnd, id):
	if id == 1024:
		from winswitch.ui.win32_balloon import notify
		notify(hwnd, "hello", "world")
	elif id == 1025:
		print("Goodbye")
		DestroyWindow(hwnd)
	else:
		print("OnCommand for ID=%s" % id)

def win32_quit():
	PostQuitMessage(0) # Terminate the app.

def main():
	iconPathName = os.path.abspath(os.path.join( sys.prefix, "pyc.ico" ))
	w=win32StatusIcon(notify_callback, win32_quit, command_callback, iconPathName)
	print("win32StatusIcon=%s" % w)
	PumpMessages()
	
if __name__=='__main__':
	main()
