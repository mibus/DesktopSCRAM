#!/usr/bin/python
import fcntl
import serial
import termios
import time
import os
import sys

while True:
	try:
		print "Trying to open a connection..."
		# Open the serial device; this is the specific USB/Serial adapter model I'm using
		s = serial.Serial('/dev/serial/by-id/usb-Prolific_Technology_Inc._USB-Serial_Controller-if00-port0')
		print "Got!"
		while True:
			print "Waiting for DTR change..."
			fcntl.ioctl(s.fd, termios.TIOCMIWAIT, (termios.TIOCM_DSR))
			# Do useful stuff
			os.system('gnome-screensaver-command -l')
			os.system('ps -C banshee > /dev/null && banshee --pause')
			# Debounce
			time.sleep(5)
	except:
		# Something died. Wait and try again.
		print "Failed. Will try again in a bit."
		print sys.exc_info()[0]
		time.sleep(30)
		pass
