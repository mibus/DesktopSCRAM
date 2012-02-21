#!/usr/bin/python
import fcntl
import serial
import termios
import time
import os

while True:
	try:
		# Open the serial device; this is the specific USB/Serial adapter model I'm using
		s = serial.Serial('/dev/serial/by-id/usb-Prolific_Technology_Inc._USB-Serial_Controller-if00-port0')
		while True:
			fcntl.ioctl(s.fd, termios.TIOCMIWAIT, (termios.TIOCM_DSR))
			dsr = s.getDSR()
			print "Got a DSR interrupt, DSR is now " % (dsr)
			# Do useful stuff
			os.system('gnome-screensaver-command -l')
			os.system('ps -C banshee && banshee --stop')
			# Debounce
			time.sleep(5)
	except:
		# Something died. Wait and try again.
		time.sleep(30)
		pass
