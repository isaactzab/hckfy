import ctypes
import re
import unicodedata

EnumWindows = ctypes.windll.user32.EnumWindows
EnumWindowsProc = ctypes.WINFUNCTYPE(ctypes.c_bool, ctypes.POINTER(ctypes.c_int), ctypes.POINTER(ctypes.c_int))
GetWindowText = ctypes.windll.user32.GetWindowTextW
GetWindowTextLength = ctypes.windll.user32.GetWindowTextLengthW
IsWindowVisible = ctypes.windll.user32.IsWindowVisible

class spotify_win():
	def __init__(self):
		pass
	def get_window_titles(self):
		titles = []
		def foreach_window(hwnd, lParam):
			if IsWindowVisible(hwnd):
				length = GetWindowTextLength(hwnd)
				buff = ctypes.create_unicode_buffer(length + 1)
				GetWindowText(hwnd, buff, length + 1)
				if (buff.value.encode("ascii", "replace").find("Spotify")  == 0 ):
					titles.append(buff.value)
					return True
			return True
		EnumWindows(EnumWindowsProc(foreach_window), 0)
		return titles

	def status(self):
		spfy_titles = self.get_window_titles()
		if(len(spfy_titles) > 0):
			wnd_caption = self.get_window_titles()[0]
			t = re.search(r"^(?P<app>Spotify)?(?P<status>\s\-\s)?(?P<nowplaying>.+)?$", wnd_caption)
			if(t != None):
				t = t.groupdict()
				t['status'] = t['status'] != None
				if(t['status']):
					nprgx = re.compile(ur"(?P<artist>[^\u2013]+)(?:\s\u2013\s)(?P<song>.+)?", re.UNICODE)
					np = nprgx.search(t['nowplaying'])
					if(np != None):
						np = np.groupdict()
						t['nowplaying'] = { 
							# "sponsor" : None,
							"artist" :unicodedata.normalize('NFKD', np['artist']).encode('ascii', 'ignore'),
							"song" : unicodedata.normalize('NFKD', np['song']).encode('ascii', 'ignore')
						}
						# if(t["nowplaying"]["artist"] in self.sponsors):
						# 	t["nowplaying"]["sponsor"] = t["nowplaying"]["artist"]
						# 	t["nowplaying"]["artist"] = None
						# 	t["nowplaying"]["Song"] = None
					else:
						# t["nowplaying"] = {"sponsor":None, "artist":None,"song":None}
						t["nowplaying"] = {"artist":None,"song":None}
				else:
					# t["nowplaying"] = {"sponsor":None, "artist":None,"song":None}
					t["nowplaying"] = {"artist":None,"song":None}
			return t
		# return {"app":False,"status":False,"nowplaying":{"sponsor":None, "artist":None,"song":None}}
		return {"app":False,"status":False,"nowplaying":{"artist":None,"song":None}}
