import ctypes
import re
import multiprocessing
import time
import unicodedata
# import os
# import sys

 
EnumWindows = ctypes.windll.user32.EnumWindows
EnumWindowsProc = ctypes.WINFUNCTYPE(ctypes.c_bool, ctypes.POINTER(ctypes.c_int), ctypes.POINTER(ctypes.c_int))
GetWindowText = ctypes.windll.user32.GetWindowTextW
GetWindowTextLength = ctypes.windll.user32.GetWindowTextLengthW
IsWindowVisible = ctypes.windll.user32.IsWindowVisible
sponsors = ["Warner"]

class Hackify(object):
	def __init__(self):
		# pass
		# print self.spfy_wnd_title()
		splited = self.spfy_nw_playing()
		if(splited):
			print splited
		else:
			print "Spotify is inactive"

	def spfy_wnd_title(self):
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

	def spfy_nw_playing(self):
		spfy_titles = self.spfy_wnd_title()
		if(len(spfy_titles) > 0):
			# wnd_caption = unicodedata.normalize('NFKD', self.spfy_wnd_title()[0]).encode('ascii','ignore')
			wnd_caption = self.spfy_wnd_title()[0]
			t = re.search(r"^(?P<app>Spotify)?(?:\s\-\s)?(?P<artist>[\w\s\'\.\-'']+)?(?:\s.\s)?(?P<song>.+)", wnd_caption)
			if(t != None):
				t = t.groupdict()
				t['app'] = unicodedata.normalize('NFKD', t['app']).encode('ascii','ignore')
				t['artist'] = unicodedata.normalize('NFKD', t['artist']).encode('ascii','ignore')
				t['song'] = unicodedata.normalize('NFKD', t['song']).encode('ascii','ignore')

				if(t['app'] == "Spotify" and t['song'] not in sponsors):
					return t
				else:
					return False
			else:
				return False
		return False

# def watchdog(HF):
# 	while 1:
# 		if(HF.spfy_wnd_title()){

# 		}
# 		try:
# 			time.sleep(1)
# 		except:
# 			continue

if __name__ == '__main__':
	Hackify()
	# wd = multiprocessing.Process(target=watchdog)
	# hf = Hackify()
	# watchdog(hf)