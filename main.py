#!/usr/bin/python
import fcntl
import serial
import signal
import termios
import time
import os
import sys

# Config
# am I on OSX or Linux?
uname = os.uname()[0]
if uname == 'Linux':
	cmd_start_screensaver = 'gnome-screensaver-command -l'
	cmd_pause_music = 'ps -C banshee > /dev/null && banshee --pause'
elif uname == 'Darwin':
	# pause iTunes (note that this always pauses; if it's not playing, it has no effect).
	# it's kinda ugly; if iTunes isn't already running, osascript will start it, then dutifully
	# tell it to pause. Gee, thanks. This should stop that.
	cmd_pause_music = '[[ -n `ps -ef | grep iTunes | grep -v grep | grep -v iTunesHelper` ]] && osascript -e \'tell application "iTunes" to pause\''
	# lock screen (which is really just "start screensaver"; you need to configure screen saver to lock the screen when it starts).
	cmd_start_screensaver = '/System/Library/Frameworks/ScreenSaver.framework/Resources/ScreenSaverEngine.app/Contents/MacOS/ScreenSaverEngine'
else:
	# do nothing.
	print 'Unable to determine OS (Linux or Darwin). Aborting.'
	sys.exit(1)

# Signal handler, just to ignore the SIGALRM we might get.
def handler(signum, frame):
	pass

signal.signal(signal.SIGALRM, handler)

# Main
while True:
	try:
		print "Trying to open a connection..."
		# Open the serial device; this is the specific USB/Serial adapter model I'm using
		last_event = time.time()
		s = serial.Serial('/dev/serial/by-id/usb-Prolific_Technology_Inc._USB-Serial_Controller-if00-port0')
		print "Got!"
		while True:
			# Check that the fd is still valid
			if not s.isOpen(): break
			# Set up a timeout, in case the device disappears for some reason
			try:
				# If we've been sitting & doing nothing for 15min, timeout in case the port has died in the meantime.
				signal.alarm(900)
				print "Waiting for DTR change..."
				fcntl.ioctl(s.fd, termios.TIOCMIWAIT, (termios.TIOCM_DSR))
				# Debounce.
				# (Also ignores events in the first 2s of runtime)
				if time.time() - last_event < 2:
					print "DTR changed, but ignored as a bounce"
					continue
				# Do useful stuff
				print "DTR changed, activating!"
				os.system(cmd_pause_music)
				os.system(cmd_start_screensaver)
				last_event = time.time();
			except IOError as e:
				if e.errno != 4: raise e
				pass
	except:
		# Something died. Wait and try again.
		print "Failed. Will try again in a bit."
		print sys.exc_info()[0]
		time.sleep(30)
		pass
