import multiprocessing
import time
from lib.spotify_win import spotify_win
from lib.audio_win import *
from lib.spotify_remote import spotify_remote

sponsors = ["Warner", "Spotify", "Warner Music", "Movistar", "Hyundai"]

class Hackify(object):
	def __init__(self):
		spotify = spotify_win(sponsors)
		remote = spotify_remote()
		audio = Audio()
		status = spotify.status()
		lastaudiostatus = True
		lastnowplaying = {}

		while 1:
			status = spotify.status()
			compare = set(lastnowplaying.items()) & set(status["nowplaying"].items())
			lastnowplaying = status["nowplaying"]
			print lastnowplaying

			# if(len(compare) == 0):
			if(status["app"] != None) and (status["nowplaying"] != None and status["nowplaying"]["sponsor"] != None):
				audio.SetMute(True)
				remote.unpause()
				lastaudiostatus = False
			elif( lastaudiostatus == False):
				audio.SetMute(False)
				lastaudiostatus = True
			try:
				time.sleep(1)
			except:
				continue



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