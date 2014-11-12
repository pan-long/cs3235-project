#!/usr/bin/python

import sys, getopt
from ui.ui_main import MainUI
from storage.preference import Arguments

def main(argv):
	try:
		opts, args = getopt.getopt(argv,"abghsdp:",["picturePath="])
	except getopt.GetoptError:
		print 'leap_motion.py [-abghps]'
		sys.exit(2)
	for opt, arg in opts:
		if opt in ("-h", "--help"):
			print 'leap_motion.py [-abghps]'
			print '-a authenticate'
			print '-b use binary authentication'
			print '-g use gesture authentication'
			print '-h print this help page'
			print '-p use picture authentication'
			print '-s set gesture for authentication'
			sys.exit()
		elif opt in ("-a", "--authentication"):
			# authentication mode
			Arguments.isSettingAuthentication = False
		elif opt in ("-b", "--binary"):
			# use left/right hand mode
			Arguments.isUsingBinaryMode = True
		elif opt in ("-g", "--gesture"):
			# use gesture mode
			Arguments.isUsingGestureMode = True
		elif opt in ("-p", "--picture"):
			# use picture mode
			Arguments.isUsingPictureMode = True
			Arguments.picturePath = arg
		elif opt in ("-s", "--set"):
			# set authentication
			Arguments.isSettingAuthentication = True
		elif opt in ("-d", "--debug"):
			Arguments.isUsingDebugMode = True
		else:
			# By default, use binary mode to set the authentication
			Arguments.isSettingAuthentication = True
			Arguments.isUsingBinaryMode = True
	
	# start the GUI
	MainUI().mainloop()

if __name__ == "__main__":
	main(sys.argv[1:])