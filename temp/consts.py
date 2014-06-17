#!/usr/bin/env python

# This file is part of Window-Switch.
# Copyright (c) 2009-2011 Antoine Martin <antoine@nagafix.co.uk>
# Window-Switch is released under the terms of the GNU GPL v3

import sys
import winswitch

DELIMITER = "\n"

APPLICATION_NAME="Window Switch"
WINSWITCH_VERSION = "%s" % winswitch.__version__
WINSWITCH_VERSION_NUMBER = winswitch.__version_number__

REQUIRED_XPRA_MIN_VERSION = [0,0,7,16]
REQUIRED_WINSWITCH_MIN_VERSION = [0,11.1]

MDNS_TYPE = '_shifter._tcp.'
REVERSED_MDNS_TYPE = '_shifter_reversed_mdns._tcp.'
UNKNOWN_APPLICATION="unknown"
ROOT_WINDOW_UUID_PROPERTY = "_WINSWITCH_UUID"						#store the owner of the display as an X root window property
ROOT_WINDOW_DESKTOPSESSION_PROPERTY = "_WINSWITCH_DESKTOPSESSION"	#store the type of session (gnome, etc) if we have it on the client
ROOT_WINDOW_SESSIONID_PROPERTY = "_WINSWITCH_SESSIONID"			#session ID of this display
ROOT_WINDOW_PULSE_SERVER = "PULSE_SERVER"

SITE_DOMAIN = "winswitch.org"
SITE_URL = "http://%s" % SITE_DOMAIN
SIGNUP_URL = "%s/signup.html" % SITE_URL
CURRENT_VERSION_URL = "%s/CURRENT_VERSION" % SITE_URL
DOWNLOAD_URL = "%s/downloads/" % SITE_URL
CHOOSE_SESSION_HELP_URL = "%s/documentation/protocols/choose.html" % SITE_URL
QUICK_CONNECT_HELP_URL = "%s/documentation/connection.html#quick" % SITE_URL
DETAILED_CONNECT_HELP_URL = "%s/documentation/connection.html#detailed" % SITE_URL

MAX_LINE_LENGTH = 1024*512

AVATAR_ICON_SIZE = 48


# useful const
LOCALHOST = "127.0.0.1"

# better to use a fixed port on win32 since we may need to allow this port through the firewall
DEFAULT_FIXED_SERVER_PORT = 32123

DEFAULT_VNC_PORT = 5900
DEFAULT_RDP_PORT = 3389

# Port offsets
PORT_START = 60
X_PORT_BASE = 6000
XNEST_OFFSET = 1000
RDP_PORT_BASE = 13000
NX_PORT_BASE = 14000
XPRA_PORT_BASE = 15000
VNC_PORT_BASE = 16000
IPP_PORT_BASE = 17000
IPP_TUNNEL_PORT_BASE = 18000
PULSE_PORT_BASE = 19000
PULSE_TUNNEL_PORT_BASE = 20000
SAMBA_TUNNEL_PORT_BASE = 21000
DISPLAY_TUNNEL_PORT_BASE = 22000
#default port for server use:
DEFAULT_SERVER_PORT = 12321
COMMAND_PORT_BASE = 12400


DEFAULT_LAN_SPEED = 100*1000*1000
DEFAULT_INTERNET_SPEED = 512*1000

NOTIFY_ERROR = "error"
NOTIFY_INFO = "info"
NOTIFY_MESSAGE = "message"
NOTIFY_AUTH_ERROR = "auth_error"
NOTIFY_RETRY = "retry"

TYPE_WORKSTATION = "workstation"
TYPE_LAPTOP = "laptop"
TYPE_SERVER = "server"

VNC_TYPE="vnc"
NX_TYPE="nx"
XPRA_TYPE="xpra"
SSH_TYPE="ssh"
X11_TYPE="X11"
WINDOWS_TYPE="windows"
OSX_TYPE="osx"
LIBVIRT_TYPE="libvirt"
SCREEN_TYPE="screen"

ALL_TYPES = [VNC_TYPE, NX_TYPE, XPRA_TYPE, SSH_TYPE, X11_TYPE, WINDOWS_TYPE, OSX_TYPE, LIBVIRT_TYPE, SCREEN_TYPE]
TYPE_NAMES = {VNC_TYPE : "VNC",
			NX_TYPE:"NX",
			XPRA_TYPE:"Xpra",
			SSH_TYPE:"SSH",
			WINDOWS_TYPE:"Windows",
			OSX_TYPE:"Mac OS X",
			LIBVIRT_TYPE:"Libvirt",
			SCREEN_TYPE:"GNU Screen"
			}
PROTOCOL_NAMES = TYPE_NAMES.copy()
PROTOCOL_NAMES[WINDOWS_TYPE] = "Remote Desktop"
PROTOCOL_NAMES[OSX_TYPE] = "Apple Remote Desktop"

PROTOCOL_CODENAMES = TYPE_NAMES.copy()
PROTOCOL_CODENAMES[WINDOWS_TYPE] = "RDP"
PROTOCOL_CODENAMES[OSX_TYPE] = "ARD"



XVNC_TIGER = "TigerVNC"
XVNC_TIGHT = "TightVNC"


# Moved here so we can reference this without referencing gtk.gdk.*_MASK:
MODIFIER_KEY_SHIFT = "Shift"



# TODO: move all of these into config?
if sys.platform.startswith("win") or sys.platform.startswith("darwin"):
	#not needed:
	DEFAULT_DISABLED_CATEGORIES = []
	DEFAULT_IGNORED_CATEGORIES = []
	DEFAULT_IGNORED_DIRECTORIES = []
	DEFAULT_IGNORED_ONLYSHOWNIN = []
	DEFAULT_IGNORED_COMMANDS = []		#not needed - would clutter the config file
	DEFAULT_IGNORED_XSESSIONS = []
	COMMANDS_WORKAROUNDS = {}
else:
	# These categories are disabled and will not be loaded
	DEFAULT_DISABLED_CATEGORIES = ["KDE", "Screensaver", "Panel"]
	# These categories aren't meaningful to the user:
	DEFAULT_IGNORED_CATEGORIES = ["", "GNOME", "GTK", "Application", "Screensaver"]
	# Absolutely no point in running a screensaver remotely!
	DEFAULT_IGNORED_DIRECTORIES = ["screensavers"]
	# Mobile applications should not be run remotely - if at all... (+double check KDE is disabled)
	DEFAULT_IGNORED_ONLYSHOWNIN = ["Mobile", "KDE"]
	# These commands would either not work, or would not be having the effect desired
	DEFAULT_IGNORED_COMMANDS = [
						# Window managers, etc:
						"compiz", "alltray", "ccsm", "avant-window-navigator", "awn-manager", "fusion-icon",
						# Ourselves!:
						"winswitch_applet",
						# stuff that binds to local devices:
						"*blueproximity*", "bluetooth*", "gpilotd-control-applet", "gsynaptics",
						"gnome-obex-server",
						# display stuff (it's not a real display!)
						"gnome-display-properties", "grandr", "*gdmsetup", "*gdmphotosetup",
						"gnome-screensaver-preferences", "resapplet",
						"*xscreensaver*",
						"*screenshot*",
						# mouse (maybe allow this?)
						"gnome-mouse-properties",
						# power should only be managed locally
						"gnome-power-preferences", "*gparted", "*jockey-gtk", "unetbootin", "usb-creator",
						# this applies to real sessions:
						"gnome-session-properties", "gnome-panel", "alacarte", "screenlets-manager",
						"gnome-appearance-properties", "onboard-settings", "gnome-window-properties", 
						# needs a real keyboard:
						"gnome-keybinding-properties", "gnome-keyboard-properties",
						# open-office does the KDE-like thing of going daemon...
						"oo*", "openoffice*",
						# behaves like a KDE app (return immediately)
						"*battery-graph*", "decibel-audio-player*",
						# needs to run locally:
						"skype",
						# goes to panel and never shows up!
						"rhythmbox*",
						# Java needs arguments
						"*javaws", "*jconsole",
						# mistakenly added as an application rather than a session:
						"openbox-session",
						# these browsers do not work via virtual desktop solutions: 
						"konqueror*", "chromium*",
						""]
	DEFAULT_IGNORED_XSESSIONS = [
							#Moblin requires GL, and none of the virtual desktop provide this extension
							"startmoblin"
							#, "openbox"	#this one may log you out of your current normal session! what the???
							]


	# These commands would not work with the command line defined in the desktop file, patch it on the fly
	COMMANDS_WORKAROUNDS = {
						"firefox" : "firefox --no-remote",
						"firefox-3.0" : "firefox-3.0 --no-remote",
						"firefox-3.5" : "firefox-3.5 --no-remote"
						}		#FIXME: uses regexp substitution...


DEFAULT_SCREEN_DEPTHS = [8,16,24]
DEFAULT_SCREEN_SIZES = [(640, 480), (800, 600), (1024, 768), (1280,1024), (1440,900), (1600, 1200), (1920,1080), (2560,1600)]
DEFAULT_SCREEN_SIZE = (1024,768)


_K = 1000
_M = _K * 1000
_G = _M * 1000

MODEM_56K_SPEED = 56*_K
DSL_256K_SPEED = 256*_K
DEFAULT_INTERNET_SPEED = _M
DEFAULT_LAN_SPEED = 100*_M
MINIMUM_LAN_SPEED = 10*_M
MAX_SPEED = 100*_G

SPEEDS = {"56 kbit/s (modem)":MODEM_56K_SPEED, "256 kbit/s": DSL_256K_SPEED, "1 Mbit/s (ADSL)": _M,
		"10 Mbit/s": 10*_M, "100 Mbit/s (LAN)": 100*_M, "1 Gbit/s": _G,
		"10 Gbit/s": 10*_G, "100 Gbit/s (local)": MAX_SPEED}
SPEED_NAMES = {}
for name,speed in SPEEDS.items():
	SPEED_NAMES[speed] = name


# generic session event constants:
# (we copy the Windows ones for now to simplify the code), see:
# http://msdn.microsoft.com/en-us/library/aa383841.aspx
CONSOLE_CONNECT = 1
CONSOLE_DISCONNECT = 2
REMOTE_CONNECT = 3
REMOTE_DISCONNECT = 4
SESSION_LOGON = 5
SESSION_LOGOFF = 6
SESSION_LOCK = 7
SESSION_UNLOCK = 8
SESSION_REMOTE_CONTROL = 9

SESSION_EVENT_NAMES = {CONSOLE_CONNECT : "Console Connect",
					CONSOLE_DISCONNECT : "Console Disconnect",
					REMOTE_CONNECT : "Remote Connect",
					REMOTE_DISCONNECT : "Remote Disconnect",
					SESSION_LOGON : "Session Logon",
					SESSION_LOGOFF : "Session Logoff",
					SESSION_LOCK : "Session Lock",
					SESSION_UNLOCK : "Session Unlock",
					SESSION_REMOTE_CONTROL : "Session Remote Control"}